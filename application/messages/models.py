from application import db
from application.models import Base

from sqlalchemy.sql import text

class Message(Base):

    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, text, user_id, thread_id):
        self.text = text
        self.account_id = user_id
        self.thread_id = thread_id

    @staticmethod
    def thread_delete_messages(thread_id):

        stmt = text("DELETE FROM Message"
                     " WHERE thread_id = :thread_id").params(thread_id=thread_id)

        db.engine.execute(stmt)