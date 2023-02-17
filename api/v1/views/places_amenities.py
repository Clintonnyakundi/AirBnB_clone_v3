#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response
import os
from models import storage


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Get amenity information on a specified place"""
    place = storage.get("Place", place_id)
    amenities_ids = place.amenities
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in amenities_ids]
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an amenity data from a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    place_amenities_ids = place.amenity_ids
    if place is None or amenity is None:
        abort(404)
    if amenity not in place_amenities_ids:
        abort(404)
    place_amenities_ids.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)