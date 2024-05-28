#!/usr/bin/python3
"""
 view for the link between Place objects and Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv
storage_type = getenv("HBNB_TYPE_STORAGE")


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id=None):
    ''' get the list of place amenities'''
    try:
        obj = storage.get("Place", place_id)
        if not obj:
            abort(404)
        amenities_list = []
        for amenity in obj:
            amenities_list.append(amenity.to_dect())
        return jsonify(amenities_list)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def delete_place_amenity(place_id=None, amenity_id=None):
    ''' Deletes a Amenity object to a Place: DELETE'''
    try:
        plcae_object = storage.get("Place", place_id)
        if not plcae_object:
            abort(404)
        amenity_object = storage.get("Place", place_id)
        if not amenity_object:
            abort(404)
        for amenity in plcae_object.amenities:
            if amenity_id == amenity.id:
                if storage_type == "db":
                    plcae_object.amenities.remove(amenity)
                else:
                    plcae_object.amenity_ids.remove(amenity_id)
        return jsonify({})
    except Exception:
        abort(404)
