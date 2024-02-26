#!/usr/bin/python3
"""This is the main flask app"""

from flask import Flask, jsonify, make_response, render_template
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(err):
    """Handles 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_db(error):
    """Handles app teardown"""
    storage.close()


if __name__ == '__main__':
    """Main function"""
    api_host = environ.get('HBNB_API_HOST')
    api_port = environ.get('HBNB_API_PORT')
    if not api_host:
        api_host = '0.0.0.0'
    if not api_port:
        api_port = 5000
    app.run(host=api_host, port=api_port, threaded=True)
