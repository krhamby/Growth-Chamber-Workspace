from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Optional
from wtforms.fields import PasswordField
from wtforms.fields import EmailField, TimeField # issue with html5

class NameForm(FlaskForm):
    name = StringField("Name: ", validators = [InputRequired()])
    submit = SubmitField("Submit")

class EmailForm(FlaskForm):
    email = EmailField("Email: ")
    password = PasswordField("Password: ")
    confirm_password = PasswordField("Confirm Password: ")

class DataChangeForm(FlaskForm):
    startTime = TimeField("Start Time: ", validators = [InputRequired()],  format = '%H:%M')
    endTime = TimeField("End Time: ", validators = [InputRequired()],  format = '%H:%M')
    submit = SubmitField("Submit")

class WaterForm(FlaskForm):
    minutes = IntegerField("Minutes: ", validators = [InputRequired()])
    interval = IntegerField("Interval (min): ", validators = [InputRequired()])
    submit = SubmitField("Submit")