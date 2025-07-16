from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class HiddenGem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    submitted_by = db.Column(db.String(100))

    def serialize(self):
        return {
            'id': self.id,
            'state': self.state,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'submitted_by': self.submitted_by
        }
# ----------------------------------------
# 🔐 Admin User for Flask-Login (In-Memory)
# ----------------------------------------
class AdminUser(UserMixin):
    def __init__(self, id):
        self.id = id

# Hardcoded Admin Credentials (username: password)
ADMIN_CREDENTIALS = {
    "manik": "manik123"   # ✅ Change to secure values
}
class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100), nullable=False)
    police = db.Column(db.String(20))
    hospital = db.Column(db.String(20))
    women_helpline = db.Column(db.String(20))

    def serialize(self):
        return {
            'state': self.state,
            'police': self.police,
            'hospital': self.hospital,
            'women_helpline': self.women_helpline
        }
