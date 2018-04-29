from application import db
from application.models import Base

from sqlalchemy.sql import text

class Tag(Base):

    name = db.Column(db.String(128), nullable=False)

    taggings = db.relationship("Tagging", backref='tag', lazy=True)

    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def tag_list():

        stmt = text("SELECT Tag.id, Tag.name FROM Tag")

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags

    @staticmethod
    def tag_list_tuple():

        stmt = text("SELECT Tag.id, Tag.name FROM Tag")

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append((row[0], row[1]))

        return tags
    
    @staticmethod
    def find_thread_id(thread_id):

        stmt = text("SELECT Tag.id, Tag.name FROM Tag"
                    " LEFT JOIN Tagging ON Tagging.tag_id = Tag.id"
                    " WHERE Tagging.thread_id=:thread_id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags

    @staticmethod
    def find_not_thread_id(thread_id):

        stmt = text("SELECT Tag.id, Tag.name FROM Tag"
                    " LEFT JOIN Tagging ON Tagging.tag_id = Tag.id"
                    " WHERE Tagging.thread_id IS NULL"
                    " OR Tagging.thread_id!=:thread_id"
                    " GROUP BY Tag.id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags