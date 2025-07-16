from flask import Blueprint, request, jsonify
from api.models import db, HiddenGem

planner_bp = Blueprint('planner', __name__)

@planner_bp.route('/api/plan-trip', methods=['POST'])
def plan_trip():
    data = request.get_json()
    state = data.get('state')
    days = int(data.get('days', 1))

    if not state or not days:
        return jsonify({"error": "Missing state or days"}), 400

    # Get hidden gems for the state
    gems = HiddenGem.query.filter_by(state=state.title()).limit(days * 2).all()

    itinerary = []
    for i in range(days):
        day_plan = {
            "day": i + 1,
            "places": [g.serialize() for g in gems[i*2:(i+1)*2]]
        }
        itinerary.append(day_plan)

    return jsonify(itinerary)
