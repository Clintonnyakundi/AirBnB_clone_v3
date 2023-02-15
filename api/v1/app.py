#!/usr/bin/python3
"""
Start API
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

# server environment setup
host = getenv("HBNB_API_HOST", '0.0.0.0')
port = getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def teardown(exc):
    """calls storage.close()
    to remove current SQLAlchemy session
    """
    storage.close()


if __name__ == '__main__':
    # starts Flask app
    app.run(host=host, port=port)
