from application import db
from application.models import Base

from sqlalchemy.sql import text

from application.auth.models import User

class Message(Base):

    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __init__(self, text, user_id=None, thread_id=None, id=None, date_created=None, date_modified=None, user=None):
        self.text = text
        self.account_id = user_id
        self.thread_id = thread_id
        self.id = id
        self.date_created = date_created
        self.date_modified = date_modified
        self.user = user

    # The argument new is included here as well for consistency.
    # I am unsure about what would be good programming style.
    def validate(self, new=False):
        return len(Message.errors(self, new=new)) == 0

    def errors(self, new=False):
        errors = []
        if len(self.text) < 1:
            errors.append("The message cannot be empty")
        return errors

    @staticmethod
    def thread_delete_messages(thread_id):

        stmt = text("DELETE FROM Message"
                     " WHERE thread_id = :thread_id").params(thread_id=thread_id)

        db.engine.execute(stmt)

    @staticmethod
    def find_thread_id(thread_id):

        stmt = text("SELECT Message.id, Message.text, Message.date_created, Message.account_id, Message.thread_id, Account.id, Account.username FROM Message"
                     " LEFT JOIN Account ON Message.account_id = Account.id"
                     " WHERE Message.thread_id = :thread_id"
                     " ORDER BY Message.date_created").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        search_result = []
        for row in res:
            user = User(id=row[5], username=row[6])
            search_result.append(Message(id=row[0], text=row[1], date_created=row[2], user_id=row[3], thread_id=row[4], user=user))

        return search_result