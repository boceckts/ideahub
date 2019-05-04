from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp

from app.services.idea_service import idea_title_exists
from app.services.user_service import username_exists, email_exists


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=64)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=1, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        if username_exists(username.data):
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email_exists(email.data):
            raise ValidationError('Please use a different email address.')


class IdeaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=128)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Engineering', 'Engineering'), ('Software Engineering', 'Software Engineering'),
        ('Science', 'Science'), ('Computer Science', 'Computer Science'),
        ('Chemistry', 'Chemistry'), ('Physics', 'Physics'),
        ('Sports', 'Sports'), ('Social', 'Social'),
        ('Lifestyle', 'Lifestyle'), ('Other', 'Other')],
                           validators=[DataRequired(), Length(min=1, max=64)])
    tags = StringField('Tags', validators=[
        Regexp(r'^$|^\w+(,\w+)*$', message='Tags have to be entered as a comma (,) separated list.')])

    def validate_title(self, title):
        if idea_title_exists(title.data):
            raise ValidationError('This idea already exists!')


class NewIdeaForm(IdeaForm):
    submit = SubmitField('Create')


class EditIdeaForm(IdeaForm):
    title = None
    submit = SubmitField('Save')


class EditProfileForm(FlaskForm):
    old_email = HiddenField('old_email')
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=64)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('New Password')
    password2 = PasswordField(
        'Repeat Password', validators=[EqualTo('password')])
    submit = SubmitField('Save')
