from application import db
from application.models import Base

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

    messages = db.relationship("Message", backref='account', lazy=True)
    taggings = db.relationship("Tagging", backref='account', lazy=True)
    reads = db.relationship("Read", backref='account', lazy=True, cascade="delete")

    def __init__(self, username, password=None, id=None):
        self.username = username
        self.password = password

    def validate(self, new=False):
        return len(User.errors(self, new=new)) == 0

    def errors(self, new=False):
        errors = []
        if len(self.username) < 1:
            errors.append("The username cannot be empty")
        if len(self.username) > 32:
            errors.append("The username must be at most 32 characters long")
        if len(self.password) < 6:
            errors.append("The password must be at least 6 characters long")
        if len(self.password) > 32:
            errors.append("The password must be at most 32 characters long")
        if new:
            if User.exists(self.username):
                errors.append("The username is taken")
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
                     " WHERE NOT Account.deleted"
                     " ORDER BY Account.username")

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

        stmt = text("SELECT Account.id FROM Account"
                     " WHERE NOT Account.deleted"
                     " AND Account.username = :username").params(username=username)

        res = db.engine.execute(stmt)

        user = res.fetchone()
        res.close()

        if user == None:
            return False

        return True

    @staticmethod
    def admin_count():
        stmt = text("SELECT COUNT(Account.id) FROM Account"
                     " WHERE Account.admin"
                     " AND (NOT Account.deleted)")

        res = db.engine.execute(stmt)

        admin_count = res.fetchone()
        res.close()

        if admin_count == None:
            return 0

        return admin_count[0]

    @staticmethod
    def user_count():
        stmt = text("SELECT COUNT(Account.id) FROM Account"
                    " WHERE (NOT Account.deleted)")

        res = db.engine.execute(stmt)

        user_count = res.fetchone()
        res.close()

        if user_count == None:
            return 0

        return user_count[0]