import bcrypt
from mongoengine import Document, StringField, BooleanField, DateTimeField, ReferenceField, ListField
from datetime import datetime
from models.user import User

class EmailRecords(Document):
    recipient = ListField(StringField(),required=True)
    subject = StringField(required=True)
    message = StringField(required = True)
    sender = StringField(required = True)
    timestamp = DateTimeField(default=datetime.utcnow)