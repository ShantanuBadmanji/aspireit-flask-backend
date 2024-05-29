from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import mongoDB
from marshmallow import Schema, ValidationError, fields

# Create a blueprint for the profile route
profile_bp = Blueprint("profile", __name__)


class ProfileSchema(Schema):
    name = fields.String()
    age = fields.Integer()


@profile_bp.route("/profile", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_profile():
    """
    Retrieve the profile data for the authenticated user.

    Returns:
        JSON response: The profile data of the user.

    Example:
        GET /profile
        Response:
        {
            "name": "John Doe",
            "age": 30
        }
    """
    email = get_jwt_identity()

    profile_data = mongoDB.users.find_one_or_404(
        {"email": email}, {"_id": 0, "password": 0}
    )

    return jsonify(profile_data), 200


@profile_bp.route("/profile", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_profile():
    """
    Update the profile data for the authenticated user.

    Returns:
        JSON response: A message indicating the success of the profile update and the updated profile data.

    Example:
        PUT /profile
        Request Body:
        {
            "name": "John Doe",
            "age": 30
        }
        Response:
        {
            "message": "Profile updated successfully",
            "updated_profile_data": {
                ...
                "name": "John Doe",
                "age": 30
            }
        }
    """
    email = get_jwt_identity()

    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    try:
        data = ProfileSchema().load(json_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 422

    mongoDB.users.update_one({"email": email}, {"$set": data})

    return (
        jsonify(
            {
                "message": "Profile updated successfully",
                "updated_profile_data": data,
            }
        ),
        200,
    )
