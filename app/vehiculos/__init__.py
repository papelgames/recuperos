from flask import Blueprint

vehiculos_bp = Blueprint('vehiculos', __name__, template_folder='templates')

from . import routes
