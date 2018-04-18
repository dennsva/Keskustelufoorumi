from application import db
from application.models import Base

class Tagging(Base):

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)

    def __init__(self, name):
        self.name = name