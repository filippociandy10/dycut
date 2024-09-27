from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import db, CuttingHistory, PaperSizes
from dycut import find_one_optimize, find_all_optimize
import os

app = Flask(__name__)
# Ensure the db directory exists inside the backend folder
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'db')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'db'))

# Configure SQLite database path relative to the backend directory
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db/cutting.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=8000, debug=True)
