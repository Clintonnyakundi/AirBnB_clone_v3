#!/usr/bin/python3
"""
Create a new view for the link between Place objects and Amenity
"""

from api.v1.views import app_views
from flask import abort, jsonify
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
