from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)
# note that the sqlalchemy session is available via api.session
# as registered in app.py

CORS(api)

@api.route('/')
def index():
    return 'API'