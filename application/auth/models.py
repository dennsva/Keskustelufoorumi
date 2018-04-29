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

    def __init__(self, username, password=None, id=None):
        self.username = username
        self.password = password

    def validate(self, new=False):
        return len(User.errors(self, new=new)) == 0

    def errors(self, new=False):
        errors = []
        if len(self.username) < 1:
            errors.append("The username cannot be empty")
        if len(self.password) < 1:
            errors.append("The password cannot be empty")
        if new:
            if User.exists(self.username):
                return errors.append("The username is taken")
        return errors

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

    @staticmethod
    def exists(username):
        # reserve the username "deleted"
        if username == "deleted":
            return True

        stmt = text("SELECT Account.id, Account.username, Account.date_created, Account.admin FROM Account"
                     " WHERE NOT Account.deleted"
                     " AND Account.username = :username").params(username=username)

        res = db.engine.execute(stmt)

        user = res.fetchone()

        if user == None:
            return False

        return True