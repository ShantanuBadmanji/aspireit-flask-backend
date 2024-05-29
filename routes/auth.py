from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import bcrypt, mongoDB
from marshmallow import Schema, ValidationError, fields

auth_bp = Blueprint("auth", __name__)


class AuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


@auth_bp.route("/register", methods=["POST"], strict_slashes=False)
def register():
    """
    Register a new user.

    This function handles the registration of a new user by receiving user data from the request,
    checking if the email already exists in the database, and saving the user data if it doesn't exist.

    Returns:
        A JSON response with a success message if the user is registered successfully,
        or an error message if the user registration fails.

    Example:
        Request:
        {
            "email": "example@example.com",
            "password": "password123"
        }

        Response (Success):
        {
            "message": "User registered successfully"
        }

        Response (Error):
        {
            "message": "User registration failed"
        }
    """
    # Get the user data from the request
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = AuthSchema().load(json_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 422

    if mongoDB.users.find_one({"email": data["email"]}):
        return jsonify({"message": "Email already exists"}), 409

    mongoDB.users.insert_one(
        {
            "email": data["email"],
            "password": bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
        }
    )

    if mongoDB.users.find_one({"email": data["email"]}):
        # Return a success message
        return jsonify({"message": "User registered successfully"}), 201

    # Return an error message
    return jsonify({"message": "User registration failed"}), 500


@auth_bp.route("/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Logs in a user with the provided email and password.

    Returns:
        A tuple containing a JSON response with a success message and an authentication token, and a status code.
        If the login is successful, the status code is 200.
        If the credentials are invalid, the status code is 401.

    Example:
        Request:
        {
            "email": "example@example.com",
            "password": "password123"
        }

        Response (Success):
        {
            "message": "User logged in successfully",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImV4YW1wbGVAZXhhbXBsZS5jb20iLCJleHAiOjE2MzI0MjM4NzAsImlhdCI6MTYzMjQyMzg3MH0.1Yz2Ry2v9Wv9X6X0J3q6Z6yj0Qb2Jzv2z2ZQ9n3z3zA"
        }

        Response (Error):
        {
            "message": "Invalid credentials"
        }
    """
    # Get the user data from the request
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = AuthSchema().load(json_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 422

    email = data.get("email")
    password = data.get("password")

    user = mongoDB.users.find_one({"email": email})
    if not user or not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=email)

    # Return a success message and authentication token
    return (
        jsonify(
            {"message": "User logged in successfully", "access_token": access_token}
        ),
        200,
    )
