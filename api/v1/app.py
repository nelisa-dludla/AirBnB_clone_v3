#!/usr/bin/python3
""" start API """
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import environ

app = Flask(__name__)

app.register_blueprint(app_views)
@app.teardown_appcontext
def teardown_appcontext(exception):
    """ method to close storage calls """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    description: resource was not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    """ runs flask server """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
