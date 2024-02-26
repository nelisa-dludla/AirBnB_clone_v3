#!/usr/bin/python3
"""
creates a new view for Amenity objects that
handles all default RESTFul API actions
"""

from models import storage
from flask import make_response, request, abort, jsonify
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route(
        '/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """retrieves list of all Amenity objects"""
    py_amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in py_amenities.values()])


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def my_amenities(amenity_id):
    """retrieves Amenity objects """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """ deletes Amenity object; if ID not linked to any
    Amenity object, raises an error"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """creates Amenity object"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """updates Amenity object, if id not linked
    to any amenities,raises an error"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    request_amenity = request.get_json()
    if not request_amenity:
        abort(400, "Not a JSON")
    for i, j in request_amenity.items():
        if i != "id" and i != "created_at" and i != "updated_at":
            setattr(amenity, i, j)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
