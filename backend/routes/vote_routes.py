from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from utils.blockchain import vote as blockchain_vote, get_votes_from_blockchain, get_candidate_votes, has_voted
from utils.database import get_db_connection

vote_bp = Blueprint('vote_bp', __name__)

@vote_bp.route('/user-info', methods=['GET'])
@login_required
def user_info():
    user_id = current_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name FROM Users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    return jsonify({"firstname": user[0]})

@vote_bp.route('/', methods=['POST'])
@login_required
def vote():
    data = request.get_json()
    candidate_id = data.get('candidate')
    if not candidate_id:
        return jsonify({"message": "candidate_id is required"}), 400

    user_id = current_user.id

    # Ghi thông tin bỏ phiếu vào blockchain
    blockchain_vote(candidate_id, user_id)

    return jsonify({"message": "Vote successful"})

@vote_bp.route('/votes', methods=['GET'])
@login_required
def get_votes():
    # Lấy danh sách phiếu bầu từ blockchain
    blockchain_votes = get_votes_from_blockchain()

    return jsonify({
        "blockchain_votes": blockchain_votes
    })

@vote_bp.route('/candidate-votes', methods=['GET'])
@login_required
def candidate_votes():
    candidate1_votes = get_candidate_votes(1)
    candidate2_votes = get_candidate_votes(2)
    return jsonify({
        "candidate1_votes": candidate1_votes,
        "candidate2_votes": candidate2_votes
    })