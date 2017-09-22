#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, sys
# from models import ExpertVolunteer, TwitterConversation, db

database_url = 'postgresql://postgres:postgres@localhost:5432/revisamigrieta_bot'
import time, sys, json
from twitter import *
from chatterbot import ChatBot
from tweet_mock import *
import list_trainer, corpora
from credentials import *

auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Twitter REST endpoint object
t = Twitter(
    auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

# Twitter User Stream endpoint object
twitter_userstream = TwitterStream(auth=OAuth(ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET),
                                   domain='stream.twitter.com')

bot = ChatBot(
    name = "Dora la coordinadora",
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",
    # input_adapter="chatterbot.input.TerminalAdapter",
    # output_adapter="chatterbot.output.TerminalAdapter",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_first_response"
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': '@revisamigrieta test',
            'output_text': 'Puedes revisar tu estructura en: http://bit.ly/RevisaMiGrieta'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'Puedo ayudarte con información para inspeccionar en: http://bit.ly/RevisaMiGrieta, espera mientras alguien te ayuda'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer'
)

list_trainer.trainer(bot,corpora.dora())


def twitter_reply(username, text):
    return "%s" % ("@%s <chatbot>: %s" % (username, text))


def get_twitter_permalink(username, tweet_id):
    return "https://twitter.com/%s/status/%s" % (username, str(tweet_id))


def retweet_with_quote(msg, text):
    permalink = get_twitter_permalink(msg["user"]["screen_name"],
                                      msg["id"])
    tweet_status = "@" + str(msg["user"]["screen_name"]) + "<chatbot>" + str(text) + str(permalink)

    t.statuses.update(status=tweet_status)
    print("Reply with quote:" + tweet_status)
    return "Reply with quote:" + tweet_status


def reply_with_bot(msg):
    bot_response = bot.get_response(msg["text"])
    tweet_status = twitter_reply(msg["user"]["screen_name"], bot_response)

    t.statuses.update(in_reply_to_status_id = msg["id"],
                      status=tweet_status)
    print("Tweeted:" + tweet_status)
    return "Tweeted:" + tweet_status, bot_response


def main(argv):

    stream = twitter_userstream.statuses.filter(track="@revisamigrieta")
    # stream = x

    for msg in stream:

        try:

            print(json.dumps(msg, sort_keys=True,indent=4, separators=(',', ': ')))
            mentions = msg["entities"]["user_mentions"]

            #
            #  Condition to match:
            #
            #    When the tweet is not a reply, not a retweet and it is not tweeted by revisamigrieta
            #

            if msg['in_reply_to_status_id'] is None and \
                            msg["retweet_count"] < 1 and \
                            msg["retweeted"] is False and \
                            msg["reply_count"] < 1 and \
                            msg["retweeted"] is False and \
                            msg["user"]["screen_name"].lower() != "revisamigrieta":


                #Reply to the user with the bot
                log_messabe, raw_bot_response = reply_with_bot(msg)

                # Retweeting with a quote to #RevisaMiGrieta
                raw_bot_response = str(raw_bot_response).lower()
                print("Raw bot response: " + raw_bot_response)

                if  "albergues" not in raw_bot_response and \
                                "#revisamigrieta" not in raw_bot_response:
                    retweet_with_quote(msg, " revisen voluntarios de #RevisaMiGrieta: ")

        except Exception as exp:

            print("There was an error: \n" + str(exp))
            pass


if __name__ == "__main__":
    main(sys.argv)
