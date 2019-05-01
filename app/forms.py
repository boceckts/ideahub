from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from app.models import User
from app.services.idea_service import idea_title_exists


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewIdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description')
    categories = SelectField('Categories', choices = [('Computing','Computing'),('DIY','DIY'),('Sport & Exercise','Sport & Exercise'),('Other','Other')], validators = [DataRequired()])
    # picture =
    submit = SubmitField('Submit')

    def validate_title(self, title):
        if idea_title_exists(title.data):
            raise ValidationError('This idea already exists!')

class EditProfileForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    surname = StringField('Surname', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired()])
    submit = SubmitField('Submit')

class EditIdeaForm(FlaskForm):
    description = StringField('Description')
    categories = SelectField('Categories', choices = [('Computing','Computing'),('DIY','DIY'),('Sport & Exercise','Sport & Exercise'),('Other','Other')], validators = [DataRequired()])
    submit = SubmitField('Submit')
