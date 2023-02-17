#!/usr/bin/python3
"""
Amenity views
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """get all amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)
