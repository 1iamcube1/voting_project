from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

from routes.auth_routes import auth_bp
from routes.vote_routes import vote_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(vote_bp, url_prefix='/api/vote')

# Serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'pages/index.html')

@app.route('/vote.html')
def serve_vote_page():
    return send_from_directory(app.static_folder, 'pages/vote.html')

@app.route('/results.html')
def serve_results_page():
    return send_from_directory(app.static_folder, 'pages/results.html')

@login_manager.user_loader
def load_user(user_id):
    from utils.database import get_db_connection
    from models.user import User
    conn = get_db_connection()
    return User.get_by_id(user_id, conn)

if __name__ == '__main__':
    app.run(port=5000)