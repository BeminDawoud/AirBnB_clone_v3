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
    if state_id:
        try:
            obj = storage.get('State', state_id).to_dict()
            return jsonify(obj)
        except Exception:
            abort(404)

    else:
        objects_list = []
        objects = storage.all("State")
        for value in objects.values():
            objects_list.append(value.to_dict())
        return jsonify(objects_list)


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
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if data:
        if "name" in data:
            obj = State(**data)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    ''' adds a new State object: POST '''
    obj = storage.get(State, state_id)
    if state_id and obj:
        try:
            data = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if data:
            for k, value in data.items():
                if (k != "id" and k != "created_at" and k != "updated_at"):
                    setattr(obj, k, value)

            obj.save()
            return (jsonify(obj.to_dict()))
        else:
            abort(400, "Not a JSON")
    else:
        abort(404)
