#!/usr/bin/python3
"""
Creates view for City objects
"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models.city import City
from models import storage


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def getCities(state_id):
    """
    Retrieves list of City objects of a State
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    allCities = list()
    for city in state.cities:
        allCities.append(city.to_dict())
    return jsonify(allCities)


@app_views.route("/cities/<city_id>/", methods=['GET'], strict_slashes=False)
def getCity(city_id):
    """
    Retrieves a city object
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>/", methods=['DELETE'],
                 strict_slashes=False)
def delete(city_id):
    """
    Deletes a City object
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create(state_id):
    """
    Creates new City object
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    new_city = request.get_json()
    if 'name' not in new_city.keys():
        abort(400, "Missing name")

    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    content['state_id'] = state_id
    city = City(**new_city)
    storage.new(city)
    storage.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=['PUT'], strict_slashes=False)
def update(city_id):
    """
    Updates City object
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    for k, v in request.get_json().items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
