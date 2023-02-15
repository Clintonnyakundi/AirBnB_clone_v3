#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """list of all State objects"""
    states = [state.to_dict() for state in storage.all("State").value()]
    return jsonify({states})
