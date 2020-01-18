from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from flaskcarleasing.models import User
from flask_login import current_user

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('This field is necessary!')])
    password = PasswordField('Password')

    first_name = StringField('First Name', validators=[DataRequired('This field is necessary!')])
    last_name = StringField('Last Name', validators=[DataRequired('This field is necessary!')])
    phone_number = StringField('Phone Number', validators=[DataRequired('This field is necessary!')])

    moderator_token = StringField('Moderator token')

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user and user != current_user:
            raise ValidationError('User with such username already exists!')

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()

        if user and user != current_user:
            raise ValidationError('User with such phone number already exists!')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Sign In')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('This field is necessary!')])
    password = PasswordField('Password')

    first_name = StringField('First Name', validators=[DataRequired('This field is necessary!')])
    last_name = StringField('Last Name', validators=[DataRequired('This field is necessary!')])
    phone_number = StringField('Phone Number', validators=[DataRequired('This field is necessary!')])

    submit = SubmitField('Sign Up')