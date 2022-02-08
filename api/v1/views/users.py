#!/usr/bin/python3
"""
New view for User objects that handles all default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def getAllUsers():
    """retrieves the list of all user objects"""
    users = []
    all_users = storage.all('User')
    for user in all_users.values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def GET_user(user_id):
    """retrieves a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def DEL_user(user_id):
    """deletes a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
        
    storage.delete(user)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def POST_user():
    """creats a new user object"""
    if not request.is_json():
        abort(400, "Not a JSON")
    if 'email' not in request.is_json():
        abort(400, "Missing email")
    if 'password' not in request.is_json():
        abort(400, "Missing password")

    new_user = User(**request.is_json())
    storage.new(new_user)
    new_user.save()
    storage.close()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def PUT_user(user_id):
    """updates a user object"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.is_json():
        abort(400, "Not a JSON")

    for key, val in request.is_json().items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, val)
    storage.save(user)
    storage.close()

    return jsonify(user.to_dict()), 200