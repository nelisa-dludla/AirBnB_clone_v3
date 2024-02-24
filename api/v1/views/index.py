#!/usr/bin/pythom3

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods = ['GET'])
def get_status():
    """ gets status of the function call """
    return jsonify(status="OK")

@app_views.route('/stats', methods = ['GET'], strict_slashes=False)
def stats():
    """ returns number of each instance in types"""
    return jsonify(amenities=storage.count("Amenity"),
            cities=storage.count("City"),
            places=storage.count("Place"),
            reviews=storage.count("REview"),
            states=storage.count("State"),
            users=storage.count("User"))
