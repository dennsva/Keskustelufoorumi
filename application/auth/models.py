from application import db

class User(db.Model):

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    messages = db.relationship("Message", backref='account', lazy=True)

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