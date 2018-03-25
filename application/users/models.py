from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
