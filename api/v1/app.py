#!/usr/bin/python3
"""
Start API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from flask_cors import CORS
import os

app = Flask(__name__)

# server environment setup
host = getenv("HBNB_API_HOST", '0.0.0.0')
port = getenv("HBNB_API_PORT", 5000)

# register blueprint
app.register_blueprint(app_views)

# create a CORS instance allowing: /* for 0.0.0.0
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exc):
    """calls storage.close()
    to remove current SQLAlchemy session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    improves 404 errors handling
    """
    content = {"error": "Not found"}
    return make_response(jsonify(content), 404)


if __name__ == '__main__':
    # starts Flask app
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
