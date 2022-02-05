#!/usr/bin/python3
"""
New view for Review object that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from os import getenv
from models.amenity import Amenity
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_amenities(place_id):
    """get amenity information for a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_id
    if amenity not in place_amenities:
        abort(404)
        
    place_amenities.remove(amenity)
    storage.save(place)
    return jsonify({})

@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_id
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    
    place_amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201