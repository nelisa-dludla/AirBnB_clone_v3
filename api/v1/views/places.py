#!/usr/bin/python3
"""
creates a new view for Place objects that
handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
import requests
import json
from os import getenv


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def places(city_id):
    """ Retrieves the list of all Place objects """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route(
        '/places/<place_id>', methods=['GET'], strict_slashes=False)
def my_place(place_id):
    """ Retrieves a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """ Deletes a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """ Creates a Place object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if "user_id" not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "name" not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route(
        '/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Updates a Place object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    request_place = request.get_json()
    if not request_place:
        abort(400, "Not a JSON")

    for i, j in request_place.items():
        if i not in ['id', 'user_id', 'city_at', 'created_at', 'updated_at']:
            setattr(place, i, j)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route(
        '/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of
    the JSON in the body of the request
    """
    request_body = request.get_json()
    if request_body is None:
        abort(400, "Not a JSON")

    if not request_body or (
            not request_body.get('states') and
            not request_body.get('cities') and
            not request_body.get('amenities')
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if request_body.get('states'):
        states = [storage.get("State", id) for id in request_body.get(
            'states')]

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if request_body.get('cities'):
        cities = [storage.get("City", id) for id in request_body.get('cities')]

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if request_body.get('amenities'):
        sln = [storage.get("Amenity", id) for id in request_body.get(
            'amenities')]
        var = 0
        search_limit = len(places)
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while var < search_limit:
            place = places[var]
            url = first_url + '{}/amenities'
            req = url.format(place.id)
            response = requests.get(req)
            done = json.loads(response.text)
            amenities = [storage.get("Amenity", j['id']) for j in done]
            for amenity in sln:
                if amenity not in amenities:
                    places.pop(var)
                    var -= 1
                    search_limit -= 1
                    break
            var += 1
    return jsonify([place.to_dict() for place in places])
