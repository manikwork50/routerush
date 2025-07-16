from flask import Blueprint, jsonify
from api.models import db, EmergencyContact

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/api/emergency/<state>', methods=['GET'])
def get_emergency_info(state):
    contact = EmergencyContact.query.filter_by(state=state.title()).first()
    if contact:
        return jsonify(contact.serialize())
    else:
        return jsonify({"error": "No emergency data found for this state"}), 404
