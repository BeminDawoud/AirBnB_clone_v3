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
