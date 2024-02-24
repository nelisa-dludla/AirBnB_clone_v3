#!/usr/bin/python3
"""
creates view of State object that handles
all default RESTFul API actions
"""

from models import storage
from models.state import State
from flask import make_response, request, jsonify, abort
from api.v1.views import app_views

@app_views.route('/states', methods = ['GET'], strict_slashes=False)
def states():
    """retrieves list of state objects"""
    rep = storage.all(State)
    return jsonify([obj.to_dict() for obj in rep.values()])

@app_views.route('/states/<state_id>', methods = ['GET'], strict_slashes=False)
def states_id(state_id):
    """retrieves state object"""
    state = storage.get("state", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods = ['DELETE'], strict_slashes=False)
def del_state(state_id):
    """deletes state object"""
    state = storage.get("state", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/state', methods = ['POST'], strict_slashes=False)
def post_state():
    """creates a state object"""
    new = request.get_json()
    if not new:
        abort(400, "Not a JSON")
    if "name" not in new:
        abort(400, "Missing name")
    state = State(**new)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/state/<state_id>', methods = ['PUT'], strict_slashes=False)
def put_state(state_id):
    """updates the state object"""
    state = storage.get("state", state_id)
    if not state:
        abort(404)
    state_request = requets.get_json()
    if not state_request:
        abort(400, "Not a JSON")
    for i, j in state_request.items():
        if i != "id" and i != "created_at" and i != "updated_at":
            setattr(state, i, j)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
