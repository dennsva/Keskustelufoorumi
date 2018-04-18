from flask_wtf import FlaskForm
from wtforms import SelectField, validators

from application.tag.models import Tag

class TaggingCreateForm(FlaskForm):
    name = SelectField("Tag this thread:", choices=Tag.tag_list())

    class Meta:
        csrf = False