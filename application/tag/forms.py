from flask_wtf import FlaskForm
from wtforms import TextField, validators

class TagCreateForm(FlaskForm):
    name = TextField("Add tag:", [validators.Length(min=1)])
 
    class Meta:
        csrf = False

class TagEditForm(FlaskForm):
    name = TextField("Name:", [validators.Length(min=1)])
 
    class Meta:
        csrf = False