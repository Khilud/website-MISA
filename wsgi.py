import os

from app import create_app

os.environ.setdefault('FLASK_ENV', 'production')

application = create_app()


if __name__ == '__main__':
    application.run()
