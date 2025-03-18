from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class ScanResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    user = db.Column(db.String(80), nullable=False)
    result = db.Column(db.String(500), nullable=False)