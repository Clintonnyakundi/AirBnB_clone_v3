#!/usr/bin/python3
"""
Create view for User object to handle all default RESTFUL API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def readUsers():
    """
    Retrieves list of all User objects
    """
    users = [user.to_dict() for user in storage.all('User').values()]
    return jsonify(users)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def readUser(user_id=None):
    """
    Retrieves a User object
    """
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("users/<user_id>", methods=['DELETE'], strict_slashes=False)
def deleteUser(user_id=None):
    """
    Deletes a User object
    """
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def createUser():
    """
    Creates a User
    """
    dict_body = request.get_json()
    if not dict_body:
        abort(400, "Not a JSON")

    if 'email' not in dict_body:
        abort(400, "Missing email")

    if 'password' not in dict_body:
        abort(400, "Missing password")

    new_user = User(**dict_body)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def updateUser(user_id=None):
    """
    Updates a User object
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    dict_body = request.get_json()
    user = storage.get('User', user_id)

    if user:
        for k, v in dict_body.items():
            if k not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, k, v)

        return make_response(jsonify(user.to_dict()), 200)
    abort(404)
