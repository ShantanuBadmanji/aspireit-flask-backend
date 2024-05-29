from io import BytesIO
import os
import time
from flask import Blueprint, jsonify, request, send_file, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import mongoDB, UPLOAD_FOLDER, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename

file_bp = Blueprint("file", __name__)


def allowed_file(filename):
    """
    Check if the file extension is allowed.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@file_bp.route("/uploads/", methods=["POST"], strict_slashes=False)
@jwt_required()
def upload_file():
    """
    Uploads a file to the server.

    Returns:
        tuple: A tuple containing a JSON response with the message and filename if the file is uploaded successfully, and the HTTP status code.
    """
    print(request.files)

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Save the file or process it as needed
        filename = secure_filename(f"{time.time()}-{file.filename}")
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return (
            jsonify({"message": "File uploaded successfully", "filename": filename}),
            200,
        )
    return "Error uploading file", 400


@file_bp.route("/uploads/<filename>/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_file(filename):
    """
    Retrieves a file from the server.

    Args:
        filename (str): The name of the file to retrieve.

    Returns:
        tuple: A tuple containing the file as a response if found, and the HTTP status code.
    """
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=False), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@file_bp.route("/uploads-mongodb/", methods=["POST"], strict_slashes=False)
@jwt_required()
def upload_file_to_mongodb():
    """
    Uploads a file to MongoDB.

    This function handles the HTTP POST request to upload a file to MongoDB. It expects the file to be included in the request payload with the key "file". The file will be saved in MongoDB along with the filename, file content, and the email of the user who uploaded it.

    Returns:
        tuple: A tuple containing a JSON response with the status of the file upload, and the HTTP status code.

    Example response:
        (
            {
                "message": "File uploaded successfully",
                "filename": "1629876543-file.txt"
            },
            200
        )
    """
    email = get_jwt_identity()

    print(request.files)

    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Save the file or process it as needed
        filename = secure_filename(f"{time.time()}-{file.filename}")
        file_content = file.read()

        if len(file_content) > MAX_CONTENT_LENGTH:
            return (
                jsonify(
                    {
                        "message": f"File size exceeds the maximum allowed size of {MAX_CONTENT_LENGTH} bytes"
                    }
                ),
                400,
            )

        mongoDB.files.insert_one(
            {"filename": filename, "content": file_content, "email": email}
        )
        return (
            jsonify({"message": "File uploaded successfully", "filename": filename}),
            200,
        )
    return "Error uploading file", 400


@file_bp.route("/uploads-mongodb/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_file_details():
    """
    Retrieves file details from MongoDB for the logged-in user.

    This function retrieves the file details from MongoDB for the user who is currently logged in.
    It uses the email associated with the JWT token to identify the user.

    Returns:
        tuple: A tuple containing a JSON response containing the file data and a status code of 200.

    Raises:
        jwt.InvalidTokenError: If the JWT token is invalid or expired.

    Example:
        If the logged-in user has uploaded two files named "file1.txt" and "file2.txt",
        the response will be a JSON object containing the filenames:
        (
            {
                "file_data": ["file1.txt", "file2.txt"]
            },
            200
        )
    """
    email = get_jwt_identity()

    # Retrieve file from MongoDB for the logged-in user
    file_data = mongoDB.files.find({"email": email}).distinct("filename")

    return jsonify(file_data), 200


@file_bp.route("/uploads-mongodb/<filename>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_file_from_mongodb(filename):
    """
    Retrieve a file from MongoDB and send it as a response.

    This function retrieves a file from MongoDB based on the provided filename and sends it as a response.
    If the file is not found in the database, a JSON response with an error message and a 404 status code is returned.

    Parameters:
    - filename (str): The name of the file to retrieve from MongoDB.

    Returns:
    - tuple: A tuple containing the file content as a response and the HTTP status code.

    Example Usage:
    GET /uploads-mongodb/myfile.txt

    Example Response:
    (
        <file_content>,
        200
    )
    """
    email = get_jwt_identity()

    # Retrieve file from MongoDB
    file_data = mongoDB.files.find_one({"filename": filename, "email": email})
    if not file_data:
        return jsonify({"error": "File not found"}), 404

    # Create a BytesIO object to hold file content
    file_content = BytesIO(file_data["content"])

    # Send file content in the response
    return (
        send_file(file_content, download_name=filename, as_attachment=False),
        200,
    )
