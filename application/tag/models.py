from application import db
from application.models import Base

from sqlalchemy.sql import text

class Tag(Base):

    name = db.Column(db.String(128), nullable=False)

    taggings = db.relationship("Tagging", backref='tag', lazy=True)

    def __init__(self, name):
        self.name = name

    def validate(self, new=False):
        return len(Tag.errors(self, new=new)) == 0

    def errors(self, new=False):
        errors = []
        if len(self.name) < 1:
            errors.append("The tag cannot be empty")
        if new:
            if Tag.exists(self.name):
                errors.append("The tag already exists")
        return errors
    
    @staticmethod
    def tag_list():
        stmt = text("SELECT Tag.id, Tag.name FROM Tag"
                    " ORDER BY Tag.name")

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags
    
    @staticmethod
    def find_thread_id(thread_id):

        stmt = text("SELECT Tag.id, Tag.name FROM Tag"
                    " LEFT JOIN Tagging ON Tagging.tag_id = Tag.id"
                    " WHERE Tagging.thread_id=:thread_id"
                    " ORDER BY Tag.name, Tag.id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags

    @staticmethod
    def find_not_thread_id(thread_id):

        stmt = text("SELECT Tag.id, Tag.name FROM Tag"
                    " WHERE Tag.id NOT IN ("
                        "SELECT Tag.id FROM Tag"
                        " LEFT JOIN Tagging ON Tagging.tag_id = Tag.id"
                        " WHERE Tagging.thread_id=:thread_id)"
                    " ORDER BY Tag.name, Tag.id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags

    @staticmethod
    def exists(name):
        stmt = text("SELECT COUNT(Tag.id) FROM Tag"
                     " WHERE Tag.name = :name").params(name=name)

        res = db.engine.execute(stmt)

        tags = res.fetchone()

        if tags == None:
            return False

        return tags[0] > 0