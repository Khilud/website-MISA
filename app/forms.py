from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional
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
    category = SelectField('Category', choices=[
        ('Documentation', 'Documentation'),
        ('Housing', 'Housing'),
        ('Language', 'Language'),
        ('Transportation', 'Transportation')
    ], validators=[DataRequired()])
    subcategory = SelectField('Subcategory', choices=[
        ('', 'Select subcategory...'),
        ('Appointments', 'Appointments'),
        ('ISEE', 'ISEE'),
        ('Residence Permit', 'Residence Permit'),
        ('Enrollment', 'Enrollment'),
        ('Permanent', 'Permanent Housing'),
        ('Temporary', 'Temporary Housing'),
        ('Italian Lessons', 'Italian Lessons'),
        ('English Lessons', 'English Lessons'),
        ('Airport Pickup', 'Airport Pickup')
    ], validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired()])
    is_available = BooleanField('Available', default=True)
    submit = SubmitField('Submit')

class ServiceRequestForm(FlaskForm):
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Special Instructions', validators=[Length(max=500)])
    submit = SubmitField('Submit Request')
    
    def __init__(self, *args, **kwargs):
        super(ServiceRequestForm, self).__init__(*args, **kwargs)
        # This will be populated in the route with available services

class UpdateRequestForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ])
    notes = TextAreaField('Admin Notes')
    submit = SubmitField('Update')