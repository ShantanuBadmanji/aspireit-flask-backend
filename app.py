from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

DEBUG = os.getenv("DEBUG", "False") == "True"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/aspireit_db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "35461648464613")

ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "png",
    "jpg",
    "jpeg",
    "gif",
    "csv",
    "xlsx",
    "docx",
    "pptx",
    "mp3",
    "mp4",
}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
mongoDB = PyMongo(app).db

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

"""
This is the main application file for the AspireIT Flask backend.

It initializes the Flask application and sets up the necessary configurations and extensions.

- `DEBUG`: A boolean indicating whether the application is in debug mode.
- `UPLOAD_FOLDER`: The path to the folder where uploaded files will be stored.
- `MONGO_URI`: The URI for connecting to the MongoDB database.
- `JWT_SECRET_KEY`: The secret key used for JWT token encryption.
- `ALLOWED_EXTENSIONS`: A set of allowed file extensions for file uploads.
- `MAX_CONTENT_LENGTH`: The maximum allowed content length for file uploads.

The Flask application is configured with the following settings:
- `MONGO_URI`: The MongoDB URI for connecting to the database.
- `JWT_SECRET_KEY`: The secret key used for JWT token encryption.

The following extensions are initialized:
- `mongoDB`: An instance of `PyMongo` for interacting with the MongoDB database.
- `bcrypt`: An instance of `Bcrypt` for password hashing.
- `jwt`: An instance of `JWTManager` for handling JWT tokens.
- `CORS`: An instance of `CORS` for enabling Cross-Origin Resource Sharing.

Note: This code assumes that the necessary environment variables are defined in a .env file.
"""
