from flask_wtf import FlaskForm
from wtforms import SelectField, validators

from application.tag.models import Tag

class TaggingCreateForm(FlaskForm):
    id = SelectField("Tag this thread:", choices=Tag.tag_list_tuple())

    class Meta:
        csrf = False