from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CuttingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_width = db.Column(db.Integer, nullable=False)
    paper_height = db.Column(db.Integer, nullable=False)
    piece_width = db.Column(db.Integer, nullable=False)
    piece_height = db.Column(db.Integer, nullable=False)
    max_pieces = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<CuttingHistory {self.id}>'

class PaperSizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_width = db.Column(db.Integer, nullable=False)
    paper_height = db.Column(db.Integer, nullable=False)

