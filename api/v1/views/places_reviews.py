#!/usr/bin/python3
"""
Create view for Review object that handles all default RESTFul API actions
"""
from api.vi.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def list_reviews(place_id=None):
    """
    Retrieves list of all Review objects of a Place
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET']
                 strict_slashes=False)
def readReview(review_id=None):
    """
    Retrieves a Review object
    """
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id=None):
    """
    Deletes a Review object
    """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def createReview(place_id=None):
    """
    Create a Review object
    """
    if not request.get_json():
        abort(400, "Not a JSON")

    dict_body = request.get_json()
    if 'user_id' not in dict_body.keys():
        abort(400, "Missing user_id")

    if 'text' not in dict_body.keys():
        abort(400, "Missing text")

    place = storage.get('Place', place_id)
    user = storage.get('User', dict_body['user_id'])

    if place and user:
        new_review = Review(**dict_body)
        new_review.place_id = place.id
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def updateReview(review_id=None):
    """
    Updates a Review object
    """
    dict_body = request.get_json()
    if not dict_body:
        abort(400, "Not a JSON")

    review = storage.get('Review', review_id)
    if review:
        for k, v in dict_body.items():
            ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
            if k not in ignore:
                setattr(review, k, v)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)
    abort(404)
