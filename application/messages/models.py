from application import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, text, user_id):
        self.text = text
        self.account_id = user_id
