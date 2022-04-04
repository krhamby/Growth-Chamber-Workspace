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
    time_data = IntegerField("Setting During Selected Time: ", validators = [InputRequired()])
    other_data = IntegerField("Setting Outside Selected Time: ", validators = [InputRequired()])
    stime = TimeField("Start Time: ", validators = [InputRequired()],  format = '%HH:%MM')
    etime = TimeField("End Time: ", validators = [InputRequired()],  format = '%HH:%MM')
    submit = SubmitField("Submit")