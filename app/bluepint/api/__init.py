from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from ....api import  auth_routes, store_routes, routes