from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Association Table (Link table) between Users and PaperSizes
user_papersizes = db.Table('user_papersizes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('papersize_id', db.Integer, db.ForeignKey('paper_sizes.id'), primary_key=True)
)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    
    # Many-to-Many relationship with PaperSizes
    paper_sizes = db.relationship('PaperSizes', secondary=user_papersizes, backref=db.backref('users', lazy=True))

    # Method to set password (hashed)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password,method='pbkdf2:sha256')

    # Method to check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
# PaperSizes model (Many-to-Many relationship with User)
class PaperSizes(db.Model):
    __tablename__ = 'paper_sizes' 
    id = db.Column(db.Integer, primary_key=True)
    paper_width = db.Column(db.Integer, nullable=False)
    paper_height = db.Column(db.Integer, nullable=False)


# CuttingHistory model
class CuttingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_width = db.Column(db.Integer, nullable=False)
    paper_height = db.Column(db.Integer, nullable=False)
    piece_width = db.Column(db.Integer, nullable=False)
    piece_height = db.Column(db.Integer, nullable=False)
    max_pieces = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

