# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    diet_type = SelectField('Dietary Preference', choices=[
        ('', 'Select Dietary Preference'),
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('paleo', 'Paleo'),
        ('ketogenic', 'Ketogenic'),
        ('gluten free', 'Gluten Free'),
        ('dairy free', 'Dairy Free'),
        ('pescatarian', 'Pescatarian')
    ])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddToMealPlanForm(FlaskForm):
    submit = SubmitField('Add to Meal Plan')


class UpdateuserForm(FlaskForm):
    username = StringField('username')
    email = EmailField('email')
    submit = SubmitField('update profile')