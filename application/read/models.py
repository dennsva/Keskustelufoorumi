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

        read = res.fetchone()
        res.close()

        if read == None:
            return 0

        return read[0]

    @staticmethod
    def unread_count(user_id, thread_id):
        return Read.messages_total(thread_id) - Read.read_count(user_id, thread_id)

    @staticmethod
    def messages_total(thread_id):
        stmt = text("SELECT COUNT(Message.id) FROM Thread"
                    " LEFT JOIN Message ON Message.thread_id = Thread.id"
                    " WHERE Thread.id = :thread_id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        messages = res.fetchone()
        res.close()

        if messages == None:
            return 0

        return messages[0]

    @staticmethod
    def mark_as_read(user_id, thread_id):
        messages = Message.find_thread_id(thread_id)
        for message in messages:
            read = Read(user_id, message.id)

            if read.exists():
                continue

            db.session().add(read)
            db.session().commit()

    def exists(self):
        stmt = text("SELECT Read.id FROM Read"
                        " WHERE Read.account_id = :account_id"
                        " AND Read.message_id = :message_id").params(account_id=self.account_id, message_id=self.message_id)

        res = db.engine.execute(stmt)

        read = res.fetchone()
        if read == None:
            return False

        return True
    
    @staticmethod
    def message_delete_read(message_id):

        stmt = text("DELETE FROM Read"
                     " WHERE message_id = :message_id").params(message_id=message_id)

        db.engine.execute(stmt)