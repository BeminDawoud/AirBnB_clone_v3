#!/usr/bin/python3
"""
handles all default RESTFul API actions for City Object
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, request, abort
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id=None):
    ''' Retrieves the list of all cities: GET'''
    city_list = []
    if state_id:
        try:
            obj = storage.get('State', state_id)
            for value in obj.cities:
                city_list.append(value.to_dict())
            return jsonify(obj)
        except Exception:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    ''' Retrieves the list of all City objects: GET'''
    if city_id:
        try:
            obj = storage.get('City', city_id)
            return jsonify(obj)
        except Exception:
            abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    ''' Deletes a City object: DELETE '''
    obj = storage.get('City', city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    ''' adds a new city object: POST '''
    state_object = storage.get('State', state_id)
    if not state_object:
        abort(404)
    try:
        data = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if data:
        if "name" in data:
            obj = City(**data)
            setattr(item, "state_id", state_id)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        else:
            abort(400, "Missing name")
    else:
        abort(400, "Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id=None):
    ''' adds a new city object: POST '''
    obj = storage.get(City, city_id)
    if city_id and obj:
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
