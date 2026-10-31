from flask import Flask
from config import Config
from models import db
from auth import auth_bp
from ticket import ticket_bp
from flask_jwt_extended import JWTManager

def create_app():
    # create flask app 
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize database 
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # set up JWT
    jwt = JWTManager(app)

    @jwt.unauthorized_loader # handles missing token 
    def missing_token_callback(reason):
        return {"error": "missing_authorization",
                "message": reason}, 401


    @jwt.invalid_token_loader # handles invalid token 
    def invalid_token_callback(reason):
        return {"error": "invalid_token",
                "message": reason}, 422

    
    @jwt.expired_token_loader # handles expired token 
    def expired_token_callback(jwt_header, jwt_data):
        return {"error": "token_expired",
                "message": "Token has expired"}, 401


    # register blueprints 
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth") # mounts auth routes 
    app.register_blueprint(ticket_bp, url_prefix="/api/v1/tickets") # mounts ticket routes 

    return app


if __name__ == "__main__":
    # run server
    app = create_app()
    app.run(debug=True)

  