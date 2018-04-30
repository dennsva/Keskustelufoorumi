from application import db
from application.models import Base

from sqlalchemy.sql import text

class Tagging(Base):

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, thread_id, tag_id, user_id):
        self.thread_id = thread_id
        self.tag_id = tag_id
        self.account_id = user_id

    def validate(self, new=False):
        return len(Tagging.errors(self, new=new)) == 0

    def errors(self, new=False):
        errors = []
        if new:
            if Tagging.exists(self.thread_id, self.tag_id):
                errors.append("The thread already has that tag")
        return errors

    @staticmethod
    def thread_delete_taggings(thread_id):

        stmt = text("DELETE FROM Tagging"
                     " WHERE thread_id = :thread_id").params(thread_id=thread_id)

        db.engine.execute(stmt)

    @staticmethod
    def tag_delete_taggings(tag_id):

        stmt = text("DELETE FROM Tagging"
                     " WHERE tag_id = :tag_id").params(tag_id=tag_id)

        db.engine.execute(stmt)

    @staticmethod
    def exists(thread_id, tag_id):
        stmt = text("SELECT COUNT(Tagging.id) FROM Tagging"
                     " WHERE Tagging.thread_id = :thread_id"
                     " AND Tagging.tag_id = :tag_id").params(thread_id=thread_id, tag_id=tag_id)

        res = db.engine.execute(stmt)

        tags = res.fetchone()

        if tags == None:
            return False

        return tags[0] > 0