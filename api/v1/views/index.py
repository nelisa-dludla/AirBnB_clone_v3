from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def status_route():
    status = { "status": "OK"}
    return jsonify(status)

@app_views.route('/stats', methods=['GET'])
def stats_route():
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

    stats =  {}
    for key, value in classes.items():
        count = storage.count(value)
        stats[key.lower()] = count
    return jsonify(stats)
