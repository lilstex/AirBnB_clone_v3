#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def getAllCities(state_id):
    """retrieves list of all cities, object of a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def getCity(city_id):
    """retrieves a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def DEL_city(city_id):
    """deletes a city body"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def POST_city(state_id):
    """creates a city object"""
    if not request.is_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
        
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    storage.new(new_city)
    new_city.save()
    storage.close()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def PUT_city(city_id):
    """updates a city object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.is_json():
        abort(400, "Not a JSON")

    for key, val in request.is_json().items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, val)
    city.save()
    storage.close()
    return jsonify(city.to_dict()), 200