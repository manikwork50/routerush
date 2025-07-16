from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class HiddenGem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
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

