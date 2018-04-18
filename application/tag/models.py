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

        stmt = text("SELECT Tag.id, Tag.name AS messages FROM Tag")

        res = db.engine.execute(stmt)

        tags = []
        for row in res:
            tags.append({"id":row[0], "name":row[1]})

        return tags