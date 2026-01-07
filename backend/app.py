from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from ticket import ticket_bp
from flask_jwt_extended import JWTManager

"""
Application bootstrap:
- Create flask app, initialize database
- Set up JWT, register blueprints, run server
"""

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)

    @jwt.unauthorized_loader # handles missing token 
    def missing_token_callback(reason):
        return {"error": "missing_authorization",
                "message": reason}, 401
    
    @jwt.invalid_token_loader # handles malformed token 
    def invalid_token_callback(reason):
        return {"error": "invalid_token",
                "message": reason}, 422
    
    @jwt.expired_token_loader # handles expired token 
    def expired_token_callback():
        return {"error": "token_expired",
                "message": "Token has expired"}


    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth") # mounts auth routes 
    app.register_blueprint(ticket_bp, url_prefix="/api/v1/tickets") # mounts ticket routes 

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

