"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode
import os

api = Blueprint('api', __name__)
get_jwt_identity
# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/user", methods=["POST"])
def register_user():
    data = request.json
    if data.get("email", None) is None:
        return jsonify({"message":"the email is required"}), 400
    

    salt = b64encode(os.urandom(32)).decode("utf-8")
    password = generate_password_hash(f"{data['password']}{salt}")
  
    
    user = User(email=data["email"], name=data["name"], password=password, salt=salt)
    db.session.add(user)

    try:
        db.session.commit()
        return jsonify({"message":"User save success"}), 201
    except Exception as error:
        print(error)
        return jsonify({"message":f"error {error}"}), 500



@api.route("/login", methods=["POST"])
def user_login():
    data = request.json
    
    if data.get("email", None) is None:
        return jsonify({"message":"the email is required"}), 400


    user = User.query.filter_by(email=data["email"]).one_or_none()
    if user is not None:
        # validar la contraseña
        result = check_password_hash(user.password, f'{data["password"]}{user.salt}')
       

        if result: 
            #generar el token
            token = create_access_token(identity=user.email)

            return jsonify({"token":token}),201
        else:
            return jsonify({"message":"bad credentials"}),400 
    else:
        return jsonify({"message":"bad credentials"}),400 


@api.route("/user", methods=["GET"])
@jwt_required()
def get_all_users():
    users = User.query.all()
    owner = get_jwt_identity()
    
    return jsonify(list(map(lambda item: item.serialize(), users))), 200