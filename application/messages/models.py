from application import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())

    text = db.Column(db.String(8096), nullable=False)

    def __init__(self, text):
        self.text = text
