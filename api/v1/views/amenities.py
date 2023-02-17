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
    amenities = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
    return jsonify(amenities)
