#!/usr/bin/python3
"""
View for State objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response
from models.state import State


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


@app_views.route("/states", methods=["POST"], strict_sladhes=False)
def post_states():
    """Creates a State"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_state = request.get_json()
    if 'name' not in new_state:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**new_state)
    state.save()
    return make_response(jsonify({state.to_dict()}), 201)
