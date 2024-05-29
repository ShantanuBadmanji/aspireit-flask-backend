from flask import jsonify

from app import DEBUG, app
from routes.profile import profile_bp
from routes.auth import auth_bp
from routes.files import file_bp
from routes.analyze import analyze_bp

app.register_blueprint(profile_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(file_bp)
app.register_blueprint(analyze_bp)


@app.route("/")
def hello():
    return jsonify({"message": "Hello, World!"}), 200


if __name__ == "__main__":
    app.run(debug=DEBUG)
