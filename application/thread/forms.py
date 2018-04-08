from flask_wtf import FlaskForm
from wtforms import TextField, validators

class ThreadCreateForm(FlaskForm):
    subject = TextField("Subject:", [validators.Length(min=1)])
    text = TextField("Message:", [validators.Length(min=1)])
 
    class Meta:
        csrf = False

class ThreadEditForm(FlaskForm):
    subject = TextField("Subject:", [validators.Length(min=1)])
    text = TextField(label="Message:", validators=[validators.Length(min=1)])

    class Meta:
        csrf = False

class ThreadSearchForm(FlaskForm):
    search_text = TextField("Search threads:", [validators.Length(min=1)])

    class Meta:
        csrf = False