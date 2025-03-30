from flask import request, jsonify
from flask_login import login_user
from models.user import User
from utils.send_email import send_email
import random
from utils.database import get_db_connection

def send_otp():
    data = request.get_json()
    cccd = data.get('cccd')
    otp = str(random.randint(100000, 999999))

    conn = get_db_connection()
    user_model = User(conn)
    try:
        user_model.create_or_update(cccd, otp)
        user = user_model.find_by_cccd(cccd)
        send_email(user['email'], 'Your OTP Code', f'Your OTP code is {otp}')
        return jsonify({"message": "OTP sent to email"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

def verify_otp():
    data = request.get_json()
    cccd = data.get('cccd')
    otp = data.get('otp')

    conn = get_db_connection()
    user_model = User(conn)
    user = user_model.find_by_cccd(cccd)

    if user and user_model.verify_otp(cccd, otp):
        user_obj = User(conn)
        user_obj.id = user['user_id']
        user_obj.first_name = user['first_name']
        login_user(user_obj)
        return jsonify({"message": "OTP verified, redirect to voting page"}), 200
    else:
        return jsonify({"message": "Invalid OTP or OTP expired"}), 400