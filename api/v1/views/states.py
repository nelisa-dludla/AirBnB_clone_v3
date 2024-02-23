from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

# This route handles GET and POST requests for States
@app_views.route('/states/', methods=['GET', 'POST'])
def states():
    if request.method == 'GET': # This checks for a GET method before running the necessary GET operation
        new_list = [] # This list will store all retrieved objects
        objs = storage.all(State)

        for _, value in objs.items():
            new_list.append(value.to_dict())

        return jsonify(new_list), 200
    elif request.method == 'POST': # This checks for a POST method before running the necessary POST operation
        data = request.get_json() # This retrieves all the URL parameters
        print(data)
        print(type(data))
        if data is None:
            abort(404, 'Not a JSON')

        if 'name' not in data:
            abort(404, 'Missing name')

        # ISSUE: The created state does not use the object data
        new_state = State(data)
        print(new_state.to_dict())
        return jsonify(new_state.to_dict()), 201
    else:
        abort(405)

@app_views.route('/states/<state_id>', methods=['GET'])
def get_states_id(state_id):
    new_list = []

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    new_list.append(obj.to_dict())
    return jsonify(new_list)

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    obj.delete()
    return {}, 200
