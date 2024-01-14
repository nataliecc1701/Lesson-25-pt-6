from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    username    = StringField("Username", validators=[InputRequired(), Length(max=20)])
    password    = PasswordField("Password", validators=[InputRequired()])
    email       = StringField("Email Address", validators=[Email(), Length(max=50)])
    first_name  = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name   = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
    