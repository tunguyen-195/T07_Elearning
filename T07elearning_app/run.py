import logging
from gevent import monkey
monkey.patch_all()

from flask_migrate import Migrate
from app import create_app
from app.extensions import db, socketio
from app.models import (
    User, Role, Course, Enrollment, LectureSession,
    Assignment, Submission, Notification
)

app = create_app()
migrate = Migrate(app, db)

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
                    handlers=[logging.StreamHandler()])

app.logger.setLevel(logging.DEBUG)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 'User': User, 'Role': Role, 'Course': Course,
        'Enrollment': Enrollment, 'LectureSession': LectureSession,
        'Assignment': Assignment, 'Submission': Submission,
        'Notification': Notification
    }

def run_server():
    app.logger.info("=== Starting Socket.IO server ===")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    run_server()

