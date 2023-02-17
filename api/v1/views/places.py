#!/usr/bin/python3
"""
Create a new view for Place objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Get places in a city on city_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)
