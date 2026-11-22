"""HTTP routes for Mini-VulnFinBot."""

from flask import Blueprint, current_app, jsonify, request

bp = Blueprint("main", __name__)

# Mock assistant: a deterministic stand-in for a real LLM.
_MOCK_RESPONSES = {
    "budget": (
        "You can start by tracking your income and expenses to see where "
        "your money goes each month."
    ),
    "save": (
        "Try setting aside a fixed percentage of each paycheck into a "
        "separate savings account."
    ),
    "debt": (
        "List your debts with their interest rates and pay down the "
        "highest-interest one first."
    ),
}
_DEFAULT_RESPONSE = (
    "I'm a mock financial assistant. I can help you think about budgeting, "
    "saving, and managing debt."
)


def _generate_response(message: str) -> str:
    """Return a canned assistant reply for a validated user message."""
    lowered = message.lower()
    for keyword, response in _MOCK_RESPONSES.items():
        if keyword in lowered:
            return response
    return _DEFAULT_RESPONSE


def register_routes(app):
    """Attach all application routes to the Flask app."""

    @app.get("/health")
    def health():
        """Liveness probe."""
        return jsonify({"status": "healthy"}), 200

    @app.post("/api/chat")
    def chat():
        """Accept a user message and return an assistant response."""
        # Reject non-JSON bodies before touching the payload.
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Request body must be a JSON object"}), 400

        message = data.get("message")
        if message is None:
            return jsonify({"error": "Missing required field: message"}), 400
        if not isinstance(message, str):
            return jsonify({"error": "Field 'message' must be a string"}), 400

        message = message.strip()
        if not message:
            return jsonify({"error": "Field 'message' must not be empty"}), 400

        max_length = current_app.config["MAX_MESSAGE_LENGTH"]
        if len(message) > max_length:
            return jsonify(
                {"error": f"Field 'message' must be at most {max_length} characters"}
            ), 400

        return jsonify({"response": _generate_response(message)}), 200