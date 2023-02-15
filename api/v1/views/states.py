#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """list of all State objects"""
    states = [state.to_dict() for state in storage.all("State").value()]
    return jsonify({states})


@app_views.route("/states/<string:state_id>",
                 methods=["GET"], Strict_slashes=False)
def get_states(state_id):
    """Retrieves a State on id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify({state.to_dict()})


@app_views.route("/states/<string:state_id>",
                 method=["DELETE"], strict_slashes=False)
def delete_states(state_id):
    """Deletes a State object on id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})
