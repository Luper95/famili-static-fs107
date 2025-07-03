"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['POST'])
def handle_members():    
    member_data = request.get_json()
    if member_data is None:
        return jsonify({"msg": "Request body is null"}), 400
    for each in ['first_name', 'age', 'lucky_numbers']:
        if each not in member_data:
            return jsonify({"msg": f"You need to specify the {each}"}), 400
    new_member = jackson_family.add_member(member_data)
    return jsonify(new_member), 200
   
   

@app.route('/members', methods=['GET'])
def handle_family():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:id>', methods=['GET'])
def handle_member(id):
    if request.method == 'GET':
        member = jackson_family.get_member(id)
        if not member:
            return jsonify({"msg": "Member not found"}), 404
        return jsonify(member), 200
   
@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete(id):   
    to_delete = jackson_family.delete_member(id)
    if to_delete:
        return jsonify({"done": True}), 200
    return jsonify({"msg": "Member not found"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
