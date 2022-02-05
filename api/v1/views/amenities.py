#!/usr/bin/python3
"""
New view for Amenity objects that handles all default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def ALL_Amenities():
    """retrieves the list of all Amenity objects"""
    amenities = []
    all_amenities = storage.all('Amenity')
    for amenity in all_amenities.values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def GET_Amenity(amenity_id):
    """retrieve an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def DEL_Amenity(amenity_id):
    """deletes an amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def POST_Amenity():
    """creates an amenity"""
    if not request.is_json():
        abort(400, "Not a JSON")
    if 'name' not in request.is_json():
        abort(400, "Missing name")

    new_amenity = Amenity(**request.is_json())
    storage.new(new_amenity)
    new_amenity.save()
    storage.close()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def PUT_Amenity(amenity_id):
    """updates an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")

    for key, val in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    storage.save(amenity)
    storage.close()

    return jsonify(amenity.to_dict()), 200