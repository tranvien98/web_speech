from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class FileAudio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), nullable=False)
    create_at = db.Column(db.String(120), nullable=False)
    path_file = db.Column(db.String(120), nullable=False)