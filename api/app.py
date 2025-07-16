from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.models import db
from api.routes.hidden_gems import hidden_gems_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register route blueprint
app.register_blueprint(hidden_gems_bp)

@app.route('/')
def home():
    return "🚀 WanderMap API is running!"

# Create tables on first run
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
