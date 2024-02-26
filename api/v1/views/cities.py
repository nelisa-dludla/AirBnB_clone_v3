#!/usr/bin/python3
"""
creates a new view for City objects that
handles all default RESTFul API actions
"""

from models import storage
from flask import make_response, request, abort, jsonify
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def cities(state_id):
    """retrieves City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route(
        '/cities/<city_id>', methods=['GET'], strict_slashes=False)
def my_city(city_id):
    """Retrieves a City object, if not linked to any city
    raises an error"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """ deletes city object; if not linked to any
    city, raises an error"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """creates a city object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")
    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route(
        '/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updates city object, if id not linked to any city,
    raises an error"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_city = request.get_json()
    if not request_city:
        abort(400, "Not a JSON")
    for i, j in request_city.items():
        if i not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, i, j)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
