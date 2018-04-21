from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators

class MessageCreateForm(FlaskForm):
    text = TextAreaField("Message:", [validators.Length(min=10)])
 
    class Meta:
        csrf = False

class MessageEditForm(FlaskForm):
    text = TextAreaField(label="Message:", validators=[validators.Length(min=1)])

    class Meta:
        csrf = False
