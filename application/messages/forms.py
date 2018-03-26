from flask_wtf import FlaskForm
from wtforms import TextField, validators

class MessageCreateForm(FlaskForm):
    text = TextField("Message:", [validators.Length(min=1)])
 
    class Meta:
        csrf = False

class MessageEditForm(FlaskForm):
    text = TextField(label="Message:", validators=[validators.Length(min=1)])

    class Meta:
        csrf = False
