# app/lecturer/__init__.py
from flask import Blueprint

bp = Blueprint('lecturer', __name__)

from app.lecturer import routes
