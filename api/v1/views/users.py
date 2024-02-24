#!/usr/bin/python3
"""
creates a new view for User objects that
handles all default RESTFul API actions
"""

from models import storage
from flask import make_response, request, abort, jsonify
from api.v1.views import app_views
from models.users import User


@app_views.route('/users', methods['GET'], strict_slashes=False)
def users():
    """retrieves list of all User objects"""
    py_user = storage.all(User)
    return jsonify([obj.to_dict() for obj in py_user.values()])


@app_views.route(
        '/users/<user_id>', methods=['GET'], strict_slashes=False)
def my_user(user_id):
    """retrieves User objects """
    user = storage.get("User",  user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """ deletes User object; if ID not linked to any
    user object, raises an error"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates User object"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route(
        '/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """updates User object, if id not linked to any  users,
    raises an error"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    request_user = request.get_json()
    if not request_user:
        abort(400, "Not a JSON")
    for i, j in request_user.items():
        if i not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, i, j)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
