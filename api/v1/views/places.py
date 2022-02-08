#!/usr/bin/python3
"""
New view for place objects that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def getAllPlaces(city_id):
    """retrieves all Place objects of City"""
    places = []
    all_places = storage.all('Place')
    get_city = storage.get("City", city_id)
    if get_city is None:
        abort(404)

    for place in all_places.values():
        if place.city_id == city_id:
            places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def getPlace(place_id):
    """returns a place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def DEL_place(place_id):
    """deletes a place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def POST_place(city_id):
    """adds a place object"""
    if not request.is_json():
        abort(400, "Not a JSON")
    if 'name' not in request.is_json():
        abort(400, "Missing name")
    if 'user_id' not in request.is_json():
        abort(400, "Missing user_id")

    user = storage.get("User", request.is_json().get('user_id'))
    if user is None:
        abort(404)

    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    new_place = Place(**request.is_json())
    new_place.city_id = city_id
    storage.new(new_place)
    new_place.save()
    storage.close()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], )
def PUT_place(place_id):
    """updates a place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.is_json():
        abort(400, "Not a JSON")

    for key, val in request.is_json().items():
        if key not in ["id", "city_id", "user_id", "created_at", "updated_at"]:
            setattr(place, key, val)
    storage.save(place)
    storage.close()
    return jsonify(place.to_dict()), 200