# Import flask and template operators
import traceback
from http import HTTPStatus

from flask import Flask, current_app
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .errors import APIError

# Define the WSGI application object
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configurations
app.config.from_object('zueribrunne.config')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# from . import models

with app.app_context():
    db.create_all()


# Import a module / component using its blueprint handler variable
from zueribrunne.fountains import fountains

# Register blueprints
app.register_blueprint(fountains)

# ERROR HANDLING
################

@app.errorhandler(APIError)
def handle_apierror(err: APIError):
    return err.msg, err.status.value

@app.errorhandler(404)
def handle_404(e):
    return handle_apierror(APIError(HTTPStatus.NOT_FOUND))

@app.errorhandler(Exception)
def handle_exception(err: Exception):
    app = current_app
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(''.join(
        traceback.format_exception(type(err), value=err, tb=err.__traceback__))
    )
    return handle_apierror(APIError(HTTPStatus.INTERNAL_SERVER_ERROR, str(err)))

@login_manager.unauthorized_handler
def unauthorized():
    raise APIError(HTTPStatus.UNAUTHORIZED)