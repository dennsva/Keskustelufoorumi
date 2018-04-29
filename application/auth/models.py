from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    messages = db.relationship("Message", backref='account', lazy=True)
    taggings = db.relationship("Tagging", backref='account', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return ["ADMIN"]

    @staticmethod
    def user_list():

        stmt = text("SELECT Account.id, Account.username, Account.date_created, Account.admin FROM Account"
                     " WHERE NOT Account.deleted")

        res = db.engine.execute(stmt)

        users = []
        for row in res:
            users.append({"id":row[0], "username":row[1], "date_created":row[2], "admin":row[3]})

        return users