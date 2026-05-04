from config.db import db

class BlockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    timestamp = db.Column(db.Float)
    data = db.Column(db.Text)
    prev_hash = db.Column(db.String(128))
    nonce = db.Column(db.Integer)
    hash = db.Column(db.String(128))