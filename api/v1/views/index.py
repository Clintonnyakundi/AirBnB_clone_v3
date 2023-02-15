#!/usr/bin/python3
"""
Returns JSON status response
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'])
def status():
    """Returns a JSON"""
    return (jsonify({"status": "OK"}))
