# app/student/__init__.py
from flask import Blueprint

bp = Blueprint('student', __name__)

from app.student import routes
