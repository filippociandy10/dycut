from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from models import db, CuttingHistory, PaperSizes, User
from dycut import find_one_optimize, find_all_optimize
from logres import RegistrationForm, LoginForm
import os

app = Flask(__name__)
# Ensure the db directory exists inside the backend folder
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'db')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'db'))

# Configure SQLite database path relative to the backend directory
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/cutting.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

CORS(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimizeall', methods=['POST'])
def optimizeAll():
    data = request.get_json()
    piece_width = int(data['piece_width'])
    piece_height = int(data['piece_height'])
    paper_sizes = PaperSizes.query.all()  
    all_max_pieces, all_min_waste, paper_width, paper_height, best_combi = find_all_optimize(piece_width,piece_height,paper_sizes)
    return jsonify({
        'all_min_waste': all_min_waste,
        'all_max_pieces': all_max_pieces,
        'paper_width': paper_width,
        'paper_height': paper_height,
        'best_combination':best_combi
    })

@app.route('/addpapersizes', methods=['POST'])
def add_paper_size():
    try:
        # Get JSON data from the request body
        data = request.get_json()
        paper_width = data['paper_width']
        paper_height = data['paper_height']
        new_paper_size = PaperSizes(paper_width=paper_width, paper_height=paper_height)

        db.session.add(new_paper_size)
        db.session.commit()

        return jsonify({
            'message': 'Paper size added successfully!',
            'id': new_paper_size.id,
            'paper_width': new_paper_size.paper_width,
            'paper_height': new_paper_size.paper_height
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    paper_width = int(data['paper_width'])
    paper_height = int(data['paper_height'])
    piece_width = int(data['piece_width'])
    piece_height = int(data['piece_height'])

    # Call the cutting logic
    best_combinations, max_pieces = find_one_optimize(
        paper_width, paper_height, piece_width, piece_height)
    
    new_entry = CuttingHistory(
        paper_width=paper_width,
        paper_height=paper_height,
        piece_width=piece_width,
        piece_height=piece_height,
        max_pieces=max_pieces
    )

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({
        'best_combinations': best_combinations,
        'max_pieces': max_pieces
    })

@app.route('/getpapersizes', methods=['GET'])
def get_paper_sizes():
    # Query all paper sizes
    paper_sizes = PaperSizes.query.all()

    # Convert the SQLAlchemy query result to a list of dictionaries
    paper_sizes_list = [{
        'id': paper.id,
        'paper_width': paper.paper_width,
        'paper_height': paper.paper_height
    } for paper in paper_sizes]
    return jsonify(paper_sizes_list)

from flask import jsonify

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from the React frontend
    username = data['username']
    password = data['password']
    confirm_password = data['confirm_password']

    # Check if passwords match
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Check if the username is already taken
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username already exists. Please choose a different one.'}), 400

    # Create the new user
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # Return a success message to the frontend
    return jsonify({'message': 'Registration successful! You can now log in.'}), 201


@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if (user.check_password(password)):
        return jsonify({'message': 'Login successful!'}), 200
    return jsonify({'error': 'Either username or password is incorrect. Please try again.'}), 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=8000, debug=True)
