# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import json, time

app = Flask(__name__)
CORS(app)

@app.route('/api/popular-routes')
def get_popular_routes():
    with open('data/popular_routes.json') as f:
        routes = json.load(f)
    return jsonify(routes)

@app.route('/api/track-search', methods=['POST'])
def track_search():
    # Save search logs (for analytic/dashboard, premium features)
    data = request.json
    # append to a file/db, analytics can be built later
    with open('data/searches.log', 'a') as f:
        f.write(f"{json.dumps({**data, 'ts': time.time()})}\n")
    return '', 204

# Extend with user favorites, deals, bookings as needed

if __name__ == "__main__":
    app.run(debug=True, port=5000)
