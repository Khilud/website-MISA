from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes import errors
    from app import models

    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.routes.service import service as service_blueprint
    app.register_blueprint(service_blueprint)

    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from app.routes.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    # Error handlers
    #from app.routes import errors
    
    return app