from flask import Flask, render_template, jsonify, Response, request, make_response
from datetime import datetime
from functools import lru_cache
import sqlite3
import os

try:
    from flask_compress import Compress
except ImportError:
    Compress = None  # optional

app = Flask(__name__, static_folder="static", template_folder="templates")

if Compress:
    Compress(app)

# ---------- DB: simple persistent counters ----------
DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = db()
    conn.execute("""
      CREATE TABLE IF NOT EXISTS visit_stats (
        key TEXT PRIMARY KEY,
        value INTEGER NOT NULL
      )
    """)
    conn.commit()
    conn.close()

def incr(key, amount=1):
    conn = db()
    cur = conn.cursor()
    cur.execute("INSERT INTO visit_stats(key,value) VALUES(?,0) ON CONFLICT(key) DO NOTHING", (key,))
    cur.execute("UPDATE visit_stats SET value = value + ? WHERE key = ?", (amount, key))
    conn.commit()
    cur.execute("SELECT value FROM visit_stats WHERE key = ?", (key,))
    val = cur.fetchone()[0]
    conn.close()
    return val

def get_val(key):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT value FROM visit_stats WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0

init_db()

# ---------- Demo data (replace with your full list) ----------
STATE_DATA = [
  {
    "slug":"rajasthan",
    "name":"Rajasthan",
    "capital":"Jaipur",
    "lang":"Hindi",
    "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Jaisalmer_Fort.jpg/1024px-Jaisalmer_Fort.jpg",
    "badge":"Forts & Desert",
    "popularity": 95
  },
  {
    "slug":"kerala",
    "name":"Kerala",
    "capital":"Thiruvananthapuram",
    "lang":"Malayalam",
    "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Alleppey_Boat_Beauty.jpg/1024px-Alleppey_Boat_Beauty.jpg",
    "badge":"Backwaters",
    "popularity": 92
  },
  {
    "slug":"assam",
    "name":"Assam",
    "capital":"Dispur",
    "lang":"Assamese",
    "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Kaziranga_Rhino.jpg/1024px-Kaziranga_Rhino.jpg",
    "badge":"Tea & Wildlife",
    "popularity": 86
  },
  {
    "slug":"ladakh",
    "name":"Ladakh",
    "capital":"Leh",
    "lang":"Ladakhi",
    "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Pangong_Tso_lake%2C_Ladakh.jpg/1024px-Pangong_Tso_lake%2C_Ladakh.jpg",
    "badge":"Himalayan Lakes",
    "popularity": 90
  },
  {
    "slug":"goa",
    "name":"Goa",
    "capital":"Panaji",
    "lang":"Konkani",
    "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Palolem_Beach%2C_Goa.jpg/1024px-Palolem_Beach%2C_Goa.jpg",
    "badge":"Beaches",
    "popularity": 93
  }
]
# TIP: add all 28 states + 8 UTs here later. Keep fields the same so the React UI "just works".


# ---------- Security headers ----------
@app.after_request
def set_headers(resp):
    resp.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    resp.headers['Permissions-Policy'] = 'geolocation=(), camera=()'
    resp.headers['Cache-Control'] = resp.headers.get('Cache-Control', 'no-store')
    return resp

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")

@lru_cache(maxsize=1)
def states_payload():
    # In real use, load from DB or JSON
    return STATE_DATA

@app.route("/api/states")
def api_states():
    resp = jsonify(states_payload())
    # cache the data for the browser
    resp.headers['Cache-Control'] = 'public, max-age=3600'
    return resp

@app.route("/api/visits", methods=["GET"])
def api_visits():
    today_key = "d:" + datetime.utcnow().strftime("%Y-%m-%d")
    return jsonify({
        "total": get_val("total"),
        "today": get_val(today_key)
    })

@app.route("/api/visits/increment", methods=["POST", "GET"])
def api_visits_increment():
    # Increment total + today's counter
    total = incr("total", 1)
    today_key = "d:" + datetime.utcnow().strftime("%Y-%m-%d")
    today = incr(today_key, 1)

    resp = make_response(jsonify({"total": total, "today": today}))
    # optional cookie just to demonstrate set-cookie; not used for logic here
    if not request.cookies.get("wm_seen"):
        resp.set_cookie("wm_seen", "1", max_age=60*60*24*365, samesite='Lax')
    return resp

if __name__ == "__main__":
    app.run(debug=True)
