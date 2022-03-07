from flask import Blueprint

compulsa_bp = Blueprint('compulsa', __name__, template_folder='templates')

from . import routes
