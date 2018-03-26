from flask_wtf import FlaskForm
from wtforms import TextField, validators

class UserCreateForm(FlaskForm):
    username = TextField("Username:", [validators.Length(min=1)])
    password = TextField("Password:", [validators.Length(min=1)])
 
    class Meta:
        csrf = False

class UserLoginForm(FlaskForm):
    username = TextField("Username:", [validators.Length(min=1)])
    password = TextField("Password:", [validators.Length(min=1)])
 
    class Meta:
        csrf = False
