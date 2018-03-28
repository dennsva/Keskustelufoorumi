from application import db

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    subject = db.Column(db.String(128), nullable=False)
    text = db.Column(db.String(8096), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    messages = db.relationship("Message", backref='thread', lazy=True)

    def __init__(self, subject, text, user_id):
        self.subject = subject
        self.text = text
        self.account_id = user_id
