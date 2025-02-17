import logging
from gevent import monkey
from logging.handlers import RotatingFileHandler
from flask import Flask, request
monkey.patch_all()

from flask_migrate import Migrate
from app import create_app
from app.extensions import db, socketio
from app.models import (
    User, Role, Enrollment, LectureSession,
    Assignment, Submission, Notification
)

app = create_app()
migrate = Migrate(app, db)

# Configure logging
if not app.debug:
    # Create a file handler object
    file_handler = RotatingFileHandler('logs/server.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)
    
    # Add the handler to the app's logger
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Server startup')

# Log each request
@app.before_request
def log_request_info():
    app.logger.info(f"Request: {request.method} {request.url}")

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 'User': User, 'Role': Role,
        'Enrollment': Enrollment, 'LectureSession': LectureSession,
        'Assignment': Assignment, 'Submission': Submission,
        'Notification': Notification
    }

def run_server():
    app.logger.info("=== Starting Socket.IO server ===")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_server()

