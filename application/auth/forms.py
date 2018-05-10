from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, validators

class UserCreateForm(FlaskForm):
    username = TextField("Username:", [validators.Length(min=1)])
    password = PasswordField("Password:", [validators.Length(min=6)])
 
    class Meta:
        csrf = False

class UserLoginForm(FlaskForm):
    username = TextField("Username:")
    password = PasswordField("Password:")
 
    class Meta:
        csrf = False
