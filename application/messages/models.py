from application import db
from application.models import Base

class Message(Base):

    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, text, user_id, thread_id):
        self.text = text
        self.account_id = user_id
        self.thread_id = thread_id
