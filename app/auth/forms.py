from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import Member


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        student = Member.query.filter_by(username=username.data).first()
        if student is not None:
            raise ValidationError('An account is already registered with this username. Please choose a different username.')

    def validate_email(self, email):
        student = Member.query.filter_by(email=email.data).first()
        if student is not None:
            raise ValidationError('An account is already registered with this email. Please register with a different email.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    remember_me = BooleanField('Remember Me')


# class SearchForm(FlaskForm):
#     search = StringField('')