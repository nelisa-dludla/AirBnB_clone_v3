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


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state(state_id):
    """retrieves all list of City objects of a State"""
    state = states_data.get(state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        state_cities = cities_data.get(state_id, [])
        return jsonify([city.to_dict() for city in state_cities])

    elif request.method == 'POST':
        """new_city = request.get_json()
        if not new_city:
            abort(400, "Not a JSON")"""
        if not request.is_json:
            abort(400, "Not a JSON")
        new_city = request.get_json()
        if "name" not in new_city:
            abort(400, "Missing name")
        city = City(**new_city)  # setattr(city, 'state_id', state_id)
        storage.new(city)
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Retrieves a City object, if not linked to any city
    raises an error"""
    city = cities_data.get(city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())

    elif request.method == 'DELETE':
        city = storage.get("City", city_id)
        if not city:
            abort(404)
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        city = storage.get("City", city_id)
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
