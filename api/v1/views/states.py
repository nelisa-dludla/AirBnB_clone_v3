#!/usr/bin/python3
"""
Creates a new view for the states route
and handles RESTful API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State

# This route handles GET and POST requests for States
@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ Handles GET and POST methods for /states"""
    if request.method == 'GET': # This checks for a GET method before running the necessary GET operation
        new_list = [] # This list will store all retrieved objects
        objs = storage.all(State)

        for _, value in objs.items():
            new_list.append(value.to_dict())

        return make_response(jsonify(new_list), 200)
    elif request.method == 'POST': # This checks for a POST method before running the necessary POST operation
        data = request.get_json() # This retrieves all the URL parameters
        if data is None:
            abort(400, 'Not a JSON')

        if 'name' not in data:
            abort(400, 'Missing name')

        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)
    else:
        abort(405)
# Below I have created one function to handle GET, DELETE and PUT methods
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def states_id(state_id):
    """
    Handles GET, DELETE, PUT methods for /states/<state_id>
    """
    if request.method == 'GET':
        new_list = []

        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)

        new_list.append(obj.to_dict())
        return make_response(jsonify(new_list), 200)

    elif request.method == 'DELETE':
        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)

        obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'PUT':
        data = request.get_json()

        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)
        if data is None:
            abort(400, 'Not a JSON')

        state_dict = obj.to_dict()
        print(state_dict)
        protected_attrs = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in protected_attrs:
                state_dict[key] = value

        print(state_dict)
        obj.delete()
        State(**state_dict).save()
        return make_response(jsonify(state_dict), 200)

    else:
        abort(405)
