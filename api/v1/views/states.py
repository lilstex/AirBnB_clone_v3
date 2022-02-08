#!/usr/bin/python3
"""
New view for City objects that handles default Restful API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def getAllStates():
    """retrieves the list of all State objects"""
    states = []
    all_states = storage.all('State')
    for item in all_states.values():
        states.append(item.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def GET_state(state_id):
    """retrieves a State object, else raise 404"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def DEL_state(state_id):
    """deletes a state object """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def POST_state():
    """creates a state, raise 400 if not valid json"""
    if not request.is_json:
        abort(400, "Not a JSON")

    if 'name' not in request.get_json():
        abort(400, "Missing name")

    new_state = State(**request.get_json())
    storage.new(new_state)

    new_state.save()
    storage.close()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def PUT_state(state_id):
    """updates a state object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if not request.is_json():
        abort(400, "Not a JSON")

    for key, val in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    storage.save(state)
    storage.close()

    return jsonify(state.to_dict())