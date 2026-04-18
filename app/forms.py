from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional, NumberRange
from app.models import User

GENDER_CHOICES = [
    ('', 'Select gender...'),
    ('female', 'Female'),
    ('male', 'Male'),
    ('non_binary', 'Non-binary'),
    ('other', 'Other'),
    ('prefer_not_to_say', 'Prefer not to say')
]

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    department = StringField('Department', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
            
    def validate_email(self, email):
        normalized_email = (email.data or '').strip()
        email.data = normalized_email
        user = User.query.filter_by(email=normalized_email).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class ProfileUpdateForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    gender = SelectField('Gender', choices=GENDER_CHOICES, validators=[Optional()])
    department = StringField('Department', validators=[Optional(), Length(max=64)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save Changes')

    def __init__(self, original_email=None, *args, **kwargs):
        self.original_email = original_email
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

    def validate_email(self, email):
        normalized_email = (email.data or '').strip()
        email.data = normalized_email

        if self.original_email and normalized_email.lower() == (self.original_email or '').strip().lower():
            return

        user = User.query.filter_by(email=normalized_email).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Documentation', 'Documentation'),
        ('Housing', 'Housing'),
        ('Language', 'Language'),
        ('Transportation', 'Transportation'),
        ('Group Tour', 'Group Tour'),
        ('Medical', 'Medical'),
        ('Career', 'Career')
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
        ('Other Language', 'Other Language'),
        ('Translation', 'Translation Service'),
        ('Airport Pickup', 'Airport Pickup'),
        ('Sicily Tour', 'Sicily Tour'),
        ('Medical Papers', 'Medical Papers'),
        ('Medical Assistance', 'Medical Assistance'),
        ('Internship', 'Internship'),
        ('Job Application', 'Job Application')
    ], validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired()])
    is_available = BooleanField('Available', default=True)
    submit = SubmitField('Submit')

class ServiceRequestForm(FlaskForm):
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    tour_cities = StringField('Preferred Cities in Sicily', validators=[Optional(), Length(max=255)])
    preferred_language = SelectField('Choose Language', choices=[
        ('', 'Select language...'),
        ('Arabic', 'Arabic'),
        ('French', 'French'),
        ('Spanish', 'Spanish'),
        ('German', 'German'),
        ('Turkish', 'Turkish'),
        ('Chinese', 'Chinese'),
        ('Other', 'Other')
    ], validators=[Optional()])
    translation_from_language = SelectField('Translate From', choices=[
        ('', 'Select source language...'),
        ('English', 'English'),
        ('Italian', 'Italian')
    ], validators=[Optional()])
    translation_to_language = SelectField('Translate To', choices=[
        ('', 'Select target language...'),
        ('English', 'English'),
        ('Italian', 'Italian')
    ], validators=[Optional()])
    notes = TextAreaField('Special Instructions', validators=[Length(max=500)])
    degree_level = StringField('Degree Level', validators=[Optional(), Length(max=64)])
    past_degree = StringField('Past Degree', validators=[Optional(), Length(max=128)])
    experience = TextAreaField('Experience', validators=[Optional(), Length(max=1000)])
    italian_language_level = SelectField('Italian Language Level', choices=[
        ('', 'Select Italian level...'),
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient'),
        ('Native', 'Native / Fluent')
    ], validators=[Optional()])
    languages = StringField('Other Languages', validators=[Optional(), Length(max=255)])
    room_type = SelectField('Type of Room', choices=[
        ('', 'Select room type...'),
        ('single', 'Single room'),
        ('shared', 'Shared room'),
        ('studio', 'Studio apartment'),
        ('apartment', 'Apartment'),
        ('any', 'Any available option')
    ], validators=[Optional()])
    housing_budget = FloatField('Monthly Budget', validators=[Optional(), NumberRange(min=0)])
    housing_preferred_location = StringField('Preferred Location', validators=[Optional(), Length(max=120)])
    housing_duration = StringField('Duration of Stay', validators=[Optional(), Length(max=80)])
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
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    notes = TextAreaField('Admin Notes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Update')


class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete User')


class EmployerWorkerRequestForm(FlaskForm):
    employer_name = StringField('Company or Contact Name', validators=[DataRequired(), Length(max=140)])
    work_category = StringField('Type of Work Needed', validators=[DataRequired(), Length(max=120)])
    work_type = SelectField('Work Duration Type', choices=[
        ('long_term', 'Long-term'),
        ('short_term', 'Short-term')
    ], validators=[DataRequired()])
    short_term_days = IntegerField('Number of Days (Short-term only)', validators=[Optional(), NumberRange(min=1, max=365)])
    preferred_start_date = DateField('Preferred Start Date', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=30)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=255)])
    details = TextAreaField('Additional Details', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Submit Employer Request')

    def validate_short_term_days(self, field):
        if self.work_type.data == 'short_term' and not field.data:
            raise ValidationError('Please provide number of days for short-term work.')


class UpdateEmployerRequestStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], validators=[DataRequired()])
    submit = SubmitField('Update')