from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
            
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    is_available = BooleanField('Available')
    submit = SubmitField('Submit')

class ServiceRequestForm(FlaskForm):
    notes = TextAreaField('Special Instructions', validators=[Length(max=500)])
    submit = SubmitField('Submit Request')

class UpdateRequestForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    notes = TextAreaField('Notes')
    submit = SubmitField('Update')