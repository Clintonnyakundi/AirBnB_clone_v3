#!/usr/bin/python3
"""
Create a new view for Place objects that handles RESTFul API actions
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request, make_response
from models.place import Place


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Get places in a city on city_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Gets information of a place on place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place on place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place"""
    city = storage.get("City", city_id)
    new_place = request.get_json()
    if city is None:
        abort(404)
    if not new_place:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in new_place:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", new_place['user_id'])
    if user is None:
        abort(404)
    if 'name' not in new_place:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place['city_id'] = city_id
    place = Place(**new_place)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update a place"""
    place = storage.get("Place", place_id)
    place_update_data = request.get_json()
    if place is None:
        abort(404)
    if not place_update_data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in place_update_data.items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """Searches for a place"""
    search_term = request.get_json()
    if search_term is not None:
        states = search_term.get('states', [])
        cities = search_term.get('cities', [])
        amenities = search_term.get('amenities', [])
        amenity_objects = [
            storage.get(
                'Amenity',
                amenity_id) for amenity_id in amenities if storage.get(
                'Amenity',
                amenity_id)]
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = [place for state_id in states
                      for city in storage.get('State', state_id).cities
                      if city.id not in cities
                      for place in storage.get('City', city.id).places]

        confirmed_places = [place.to_dict() for place in places if all(
            amenity in place.amenities for amenity in amenity_objects)]
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
