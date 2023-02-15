#!/usr/bin/python3
"""
Returns JSON status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


hbnb_objects = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route("/status", methods=['GET'])
def status():
    """Returns a JSON"""
    if request.method == 'GET':
        return (jsonify({"status": "OK"}))


@app_views.route("/stats", methods=["GET"])
def hbnbStats():
    """Retrieves the number of each objects"""
    return_dict = {}
    for key, value in hbnb_objects.items():
        return_dict[key] = storage.count(value)
    return jsonify({return_dict})
