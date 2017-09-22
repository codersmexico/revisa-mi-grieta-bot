def trainer(bot, corpora):
    for conversation in corpora:
        bot.train(conversation)