from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.models import db
from api.routes.hidden_gems import hidden_gems_bp
from api.routes.emergency import emergency_bp  # <-- add this

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register route blueprints
app.register_blueprint(hidden_gems_bp)
app.register_blueprint(emergency_bp)

@app.route('/')
def home():
    return "🚀 WanderMap API is running!"

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
