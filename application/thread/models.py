from application import db
from application.models import Base

from sqlalchemy.sql import text

class Thread(Base):

    subject = db.Column(db.String(128), nullable=False)
    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    messages = db.relationship("Message", backref='thread', lazy=True)

    def __init__(self, subject, text, user_id):
        self.subject = subject
        self.text = text
        self.account_id = user_id

    @staticmethod
    def search_thread(search_text):

        search_text_param = "%" + search_text + "%"

        stmt = text("SELECT Thread.id, Thread.subject, Thread.date_created, Thread.account_id, Account.username FROM Thread"
                     " LEFT JOIN Account ON Thread.account_id = Account.id"
                     " WHERE Thread.subject LIKE :search_text_param").params(search_text_param=search_text_param)

        res = db.engine.execute(stmt)

        search_result = []
        for row in res:
            search_result.append({"id":row[0], "subject":row[1], "date_created":row[2], "user_id":row[3], "username":row[4]})

        return search_result

    @staticmethod
    def thread_list():

        stmt = text("SELECT Thread.id, Thread.subject, Thread.date_created, Thread.account_id, Account.username FROM Thread"
                     " LEFT JOIN Account ON Thread.account_id = Account.id")

        res = db.engine.execute(stmt)

        threads = []
        for row in res:
            threads.append({"id":row[0], "subject":row[1], "date_created":row[2], "user_id":row[3], "username":row[4]})

        return threads