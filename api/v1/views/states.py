#!/usr/bin/python3
"""
handles all default RESTFul API actions for State Object
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    ''' Retrieves the list of all State objects: GET'''
    tmp_obj = []
    if not state_id:
        for val in storage.all(State).values():
            tmp_obj.append(val.to_dict())
        return jsonify(tmp_obj)
    item = storage.get(State, state_id)
    if item:
        return jsonify(item.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    ''' Deletes a State object: DELETE '''
    obj = storage.get('State', state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    ''' adds a new State object: POST '''
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    state_name = data.get("name", None)
    if not state_name:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    ''' adds a new State object: POST '''
    obj = storage.get('State', state_id)
    if not obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if (key != "id" and key != "created_at" and key != "updated_at"):
            setattr(obj, key, value)
    obj.save()
    return jsonify(obj.to_dict()), 200
