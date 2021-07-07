from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired


class SignUpForm(FlaskForm):
    inputFirstName = StringField('First name',
                                 [DataRequired(message="Please enter your first name")])
    inputLastName = StringField('Last name',
                                [DataRequired(message="Please enter your last name")])
    inputEmail = StringField('Email address',
                             [Email(message='Not a valid email address'),
                              DataRequired(message="Please enter your email address")])
    inputPassword = PasswordField('Password',
                                  [InputRequired(message="Please enter your password!"),
                                   EqualTo('inputConfirmPassword', message="Passwords does not match!!")])
    inputConfirmPassword = PasswordField('Confirm password')
    submit = SubmitField('Sign Up')

class SignInForm(FlaskForm):
    inputEmail = StringField('Email address',
                             [Email(message="Not a vaild email address"),
                              DataRequired(message="Please enter your email address!!!")])
    inputPassword = PasswordField('Password',
                                  [InputRequired(message="Please enter your password!!!")])
    submit = SubmitField('Sign In')

class TaskForm(FlaskForm):
    inputName = StringField('Name',
                            [InputRequired(message="Please enter your project name!")])
    inputDescription = StringField('Description',
                                   [InputRequired(message="Please enter your description!")])
    inputDeadline = DateTimeLocalField('Project deadline',
                                       validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Create Task')

class ProjectForm(FlaskForm):
    inputName = StringField('Name',
                            [InputRequired(message="Please enter your project name!")])
    inputDescription = StringField('Description',
                                   [InputRequired(message="Please enter your description!")])
    inputDeadline = DateTimeLocalField('Project deadline',
                                       validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Create Project')

class EditTaskForm(FlaskForm):
    inputDescription = StringField('Description',
                                   [InputRequired(message="Please enter your description!")])
    inputPriority = IntegerField('Priority',
                                 [InputRequired(message="Please enter task priority with number!")])
    submit = SubmitField('Edit')