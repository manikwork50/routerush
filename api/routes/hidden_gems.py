from flask import Blueprint, request, jsonify
from api.models import db, HiddenGem

hidden_gems_bp = Blueprint('hidden_gems', __name__)

@hidden_gems_bp.route('/api/hidden-gems/<state>', methods=['GET'])
def get_hidden_gems(state):
    gems = HiddenGem.query.filter_by(state=state.title()).all()
    return jsonify([gem.serialize() for gem in gems])

@hidden_gems_bp.route('/api/hidden-gems', methods=['POST'])
def submit_hidden_gem():
    data = request.get_json()
    
    required_fields = ['state', 'name', 'description', 'submitted_by']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    gem = HiddenGem(
        state=data['state'].title(),
        name=data['name'],
        description=data['description'],
        image_url=data.get('image_url', ''),
        submitted_by=data['submitted_by']
    )
    db.session.add(gem)
    db.session.commit()
    return jsonify({"status": "success", "id": gem.id}), 201

