import datetime
from sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#
#   ExpertVolunteer
#
#   A Model for registering a volunteer
#       id: (Auto generated) Unique id.
#       twitter_handle = the username in twitter of the user.
#       busy = a flag for marking a user busy helping out
#       login_status = to know if the user is available for helping
#       timestamp = When was this user registered
#

class ExpertVolunteer(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    twitter_handle = db.Column(db.String(64), nullable=False, index=True)
    busy = db.Column(db.Float, nullable=False)
    login_status = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

#
#   TwitterConversation
#
#   A Model for saving a conversation going on on twitter
#
#       id: (Auto generated) Unique id.
#       username: The name of the user to identify who is measuring.
#       location: Geolocalization of the user.
#       mode_of_transportation: The mode of transportation provided by the user.
#       warning_text: The text generated to alert the driver.
#       timestamp: (Auto generated) UTC time stamp of the event
#

class TwitterConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expert_handle = db.Column(db.String(64), nullable=False, index=True)
    requester_handle = db.Column(db.String(64), index=True, nullable=False)
    conversation_id = db.Column(db.String(64), index=True, nullable=False)
    start_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    stop_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)