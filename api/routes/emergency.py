from flask import Blueprint, request, jsonify

emergency_bp = Blueprint('emergency', __name__)

# Sample emergency contact data
emergency_data = {
    "rajasthan": {
        "police": "100",
        "ambulance": "108",
        "fire": "101"
    },
    "uttar pradesh": {
        "police": "100",
        "ambulance": "102",
        "fire": "101"
    },
    "maharashtra": {
        "police": "100",
        "ambulance": "108",
        "fire": "101"
    },
    # Add more states as needed
}

@emergency_bp.route('/api/emergency-info')
def emergency_info():
    state = request.args.get("state", "").strip().lower()
    if state in emergency_data:
        return jsonify(success=True, info=emergency_data[state])
    return jsonify(success=False, message="State not found")
