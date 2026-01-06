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

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(ticket_bp, url_prefix="/api/v1/tickets")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

