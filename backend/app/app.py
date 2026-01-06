from flask import Flask
from flask_cors import CORS 
from config import Config
from models import db 
from auth import auth_bp 
from ticket import ticket_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ticket_bp, url_prefix="/api/tickets")
    return app

if __name__ == "__main__":
    create_app.run(debug=True)

