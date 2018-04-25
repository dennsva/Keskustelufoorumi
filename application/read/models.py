from application import db
from application.models import Base

from sqlalchemy.sql import text

from application.messages.models import Message

class Read(Base):

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)

    def __init__(self, user_id, message_id):
        self.account_id = user_id
        self.message_id = message_id

    @staticmethod
    def read_count(user_id, thread_id):
        stmt = text("SELECT COUNT(Read.message_id) FROM Read"
                     " LEFT JOIN Message ON Message.id = Read.message_id"
                     " LEFT JOIN Thread ON Thread.id = Message.thread_id"
                     " WHERE Read.account_id = :account_id"
                     " AND Thread.id = :thread_id").params(account_id=user_id, thread_id=thread_id)

        res = db.engine.execute(stmt)

        if res is None:
            return 0

        for row in res:
            read=row[0]
            break

        return read

    @staticmethod
    def unread_count(user_id, thread_id):
        return Read.messages_total(thread_id) - Read.read_count(user_id, thread_id)

    @staticmethod
    def messages_total(thread_id):
        stmt = text("SELECT COUNT(Message.id) FROM Thread"
                    " LEFT JOIN Message ON Message.thread_id = Thread.id"
                    " WHERE Thread.id = :thread_id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        if res is None:
            return 0

        for row in res:
            messages=row[0]
            break

        return messages

    @staticmethod
    def mark_as_read(user_id, thread_id):
        messages = Message.find_thread_id(thread_id)
        for message in messages:
            stmt = text("INSERT INTO Read (account_id, message_id) VALUES (:account_id, :message_id)").params(account_id=user_id, message_id=message["id"])

            db.engine.execute(stmt)