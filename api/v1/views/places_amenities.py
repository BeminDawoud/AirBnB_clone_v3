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
        for amenity in obj.amenities:
            amenities_list.append(amenity.to_dect())
        return jsonify(amenities_list)
    except Exception:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id=None, amenity_id=None):
    ''' Deletes an Amenity object from a Place: DELETE'''
    place_object = storage.get("Place", place_id)
    if not place_object:
        abort(404)
    if not storage.get("Amenity", amenity_id):
        abort(404)

    found = False
    for amenity in place_object.amenities:
        if amenity_id == amenity.id:
            found = True
            if storage_type == "db":
                place_object.amenities.remove(amenity)
            else:
                place_object.amenity_ids.remove(amenity_id)
            place_object.save()
            break

    if found:
        return jsonify({}), 200
    else:
        abort(404)
