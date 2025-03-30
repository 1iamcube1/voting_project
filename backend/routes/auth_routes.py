from flask import Blueprint, request, jsonify
from flask_login import login_user
from controllers.auth_controller import send_otp, verify_otp
from utils.database import get_db_connection
from models.user import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/send-otp', methods=['POST'])
def send_otp_route():
    return send_otp()

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    return verify_otp()