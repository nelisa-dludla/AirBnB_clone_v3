from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.errorhandler(404)
def error_route(err):
    error = { "error": "Not found"}
    return jsonify(error), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == '__main__':
    api_host = environ.get('HBNB_API_HOST', '0.0.0.0')
    api_port = int(environ.get('HBNB_API_PORT', 5000))

    app.run(host=api_host, port=api_port, threaded=True)
