from flask import Blueprint

ofrecimiento_bp = Blueprint('ofrecimiento', __name__, template_folder='templates')

from . import routes
