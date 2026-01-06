from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from ticket import ticket_bp
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return {"error": "missing_authorization",
                "message": reason}, 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return {"error": "invalid_token",
                "message": reason}, 422
    
    @jwt.expired_token_loader
    def expired_token_callback():
        return {"error": "token_expired",
                "message": "Token has expired"}


    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(ticket_bp, url_prefix="/api/v1/tickets")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

