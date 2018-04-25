from application import db
from application.models import Base

from sqlalchemy.sql import text

from application.read.models import Read
from flask_login import current_user

class Thread(Base):

    subject = db.Column(db.String(128), nullable=False)
    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    messages = db.relationship("Message", backref='thread', lazy=True)
    taggings = db.relationship("Tagging", backref='thread', lazy=True)

    def __init__(self, subject, text, user_id):
        self.subject = subject
        self.text = text
        self.account_id = user_id

    @staticmethod
    def search_thread(search_text):

        search_text_param = "%" + search_text + "%"

        stmt = text("SELECT Thread.id, Thread.subject, Thread.date_created, Thread.account_id, Account.username, COUNT(Message.id) AS messages FROM Thread"
                     " LEFT JOIN Account ON Thread.account_id = Account.id"
                     " LEFT JOIN Message ON Thread.id = Message.thread_id"
                     " WHERE Thread.subject LIKE :search_text_param"
                     " GROUP BY Thread.id, Account.username").params(search_text_param=search_text_param)

    # postgresql vaatii tuon Account.username lopussa.
    # Se ei vaikuta kyselyyn mitenkään, sillä viestiketjun
    # aloittaja on yksikäsitteinen.
    
        res = db.engine.execute(stmt)

        search_result = []
        for row in res:
            search_result.append({"id":row[0], "subject":row[1], "date_created":row[2], "user_id":row[3], "username":row[4], "messages":row[5]})

        return search_result

    @staticmethod
    def thread_list():

        stmt = text("SELECT Thread.id, Thread.subject, Thread.date_created, Thread.account_id, Account.username, COUNT(Message.id) AS messages FROM Thread"
                     " LEFT JOIN Account ON Thread.account_id = Account.id"
                     " LEFT JOIN Message ON Thread.id = Message.thread_id"
                     " GROUP BY Thread.id, Account.username")

        res = db.engine.execute(stmt)

        threads = []
        for row in res:
            threads.append({"id":row[0], "subject":row[1], "date_created":row[2], "user_id":row[3], "username":row[4], "messages":row[5]})

        for thread in threads:
            if current_user.is_authenticated:
                thread["unread"] = Read.unread_count(current_user.id, thread["id"])
            else:
                thread["unread"] = thread["messages"]

        return threads

    @staticmethod
    def find_tag_id(tag_id):

        stmt = text("SELECT Thread.id, Thread.subject, Thread.date_created, Thread.account_id, Account.username, COUNT(Message.id) AS messages FROM Thread"
                     " LEFT JOIN Account ON Thread.account_id = Account.id"
                     " LEFT JOIN Message ON Thread.id = Message.thread_id"
                     " LEFT JOIN Tagging ON Tagging.thread_id = Thread.id"
                     " WHERE Tagging.tag_id = :tag_id"
                     " GROUP BY Thread.id, Account.username").params(tag_id=tag_id)

        res = db.engine.execute(stmt)

        search_result = []
        for row in res:
            search_result.append({"id":row[0], "subject":row[1], "date_created":row[2], "user_id":row[3], "username":row[4], "messages":row[5]})

        for thread in search_result:
            if current_user.is_authenticated:
                thread["unread"] = Read.unread_count(current_user.id, thread["id"])
            else:
                thread["unread"] = thread["messages"]

        return search_result