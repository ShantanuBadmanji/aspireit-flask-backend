from flask import Blueprint, request, jsonify
import joblib
from marshmallow import Schema, ValidationError, fields


analyze_bp = Blueprint("ml_model", __name__)

ml_model = joblib.load("ml-model/sentement_analysis_joblib")


class AnalyzeSchema(Schema):
    text = fields.String(required=True)


@analyze_bp.route("/analyze", methods=["POST"], strict_slashes=False)
def analyze():
    """
    Analyzes the sentiment of the given text.

    This route accepts a POST request with a JSON payload containing the 'text' field.
    It validates the input using the AnalyzeSchema and returns a JSON response with the sentiment prediction.

    Returns:
        A JSON response containing the sentiment prediction.
        {
            "message": "Analyze route",
            "prediction": "positive" or "negative" or "neutral"
        }

    Raises:
        400 Bad Request: If the 'text' field is missing or empty in the request.
        422 Unprocessable Entity: If the input data fails validation against the AnalyzeSchema.
    """
    # Get the user data from the request
    json_data = request.get_json()
    if not json_data or "text" not in json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = AnalyzeSchema().load(json_data)
    except ValidationError as err:
        return jsonify({"message": err.messages}), 422

    # Get the text from the request
    text = data["text"]
    if text == "":
        return jsonify({"message": "Text is required"}), 400

    # predict the sentiment of the text
    prediction = ml_model.predict(text)
    return jsonify({"message": "Analyze route", "prediction": prediction}), 200
