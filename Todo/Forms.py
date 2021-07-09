from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from Todo.Models import User


class AddTodoForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username Already Exist, Try Another One")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email Address Already Exist, Try Another one")

    title = StringField(label="Enter The Title", validators=[Length(max=30), DataRequired()])
    description = StringField(label="Enter Description", validators=[Length(max=500), DataRequired()])
    submit = SubmitField(label="Add Todo")


class RegisterForm(FlaskForm):
    username = StringField(label="Enter Your Name", validators=[Length(min=5, max=15), DataRequired()])
    email_address = StringField(label="Enter Email_Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Enter Password", validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label="Confirm your Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    email_address = StringField(label="Enter Email Address", validators=[DataRequired()])
    password = PasswordField(label="Enter Password", validators=[DataRequired()])
    submit = SubmitField(label="SignIn")


class UpdateForm(FlaskForm):
    title = StringField(label="Enter The Title", validators=[Length(max=30), DataRequired()])
    description = StringField(label="Enter Description", validators=[Length(max=500), DataRequired()])
    submit = SubmitField(label="Update")
