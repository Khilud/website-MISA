from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, index=True)
    phone_number = db.Column(db.String(20))
    department = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    requests = db.relationship('ServiceRequest', backref='client', lazy='dynamic')

    @property
    def full_name(self):
        first = (self.first_name or '').strip()
        last = (self.surname or '').strip()
        return f'{first} {last}'.strip()

    @property
    def display_name(self):
        return self.full_name or self.email or self.username or f'User {self.id}'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.display_name}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50))
    price = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True)
    requests = db.relationship('ServiceRequest', backref='service_type', lazy='dynamic')
    
    def __repr__(self):
        return f'<Service {self.name}>'

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    status = db.Column(db.String(20), default='pending')  # pending, approved, completed, cancelled
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    degree_level = db.Column(db.String(64), nullable=True)
    past_degree = db.Column(db.String(128), nullable=True)
    experience = db.Column(db.Text, nullable=True)
    italian_language_level = db.Column(db.String(20), nullable=True)
    languages = db.Column(db.String(255), nullable=True)
    requester_full_name = db.Column(db.String(140), nullable=True)

    @property
    def requester_name(self):
        if self.requester_full_name:
            return self.requester_full_name
        if self.client:
            return self.client.display_name
        return f'User ID {self.user_id}' if self.user_id else 'Unknown'
    
    def __repr__(self):
        return f'<ServiceRequest {self.id}>'


class EmployerWorkerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employer_name = db.Column(db.String(140), nullable=False)
    work_category = db.Column(db.String(120), nullable=False)
    work_type = db.Column(db.String(20), nullable=False)
    short_term_days = db.Column(db.Integer, nullable=True)
    preferred_start_date = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone_number = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    details = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def work_type_label(self):
        return 'Long-term' if self.work_type == 'long_term' else 'Short-term'

    def __repr__(self):
        return f'<EmployerWorkerRequest {self.id}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))