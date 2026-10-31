from flask import Flask                        # web framework
from config import Config                      # settings (secrets, database, token lifetime)
from models import db                          # shared database object 
from auth import auth_bp                       # blueprint for /register, /login, /all
from ticket import ticket_bp                   # blueprint for ticket routes 
from flask_jwt_extended import JWTManager      # adds JWT login support to Flask

def create_app(): # "application factory": builds and returns a fresh app each call 

    # create flask app 
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize database 
    db.init_app(app) # connects database object to this app
    with app.app_context():
        db.create_all() # create any missing tables

    # set up JWT
    jwt = JWTManager(app)

    # three handlers replace flask-jwt-extended's default error responses 
    # so every token probelm returns a JSON message 

    @jwt.unauthorized_loader # handles missing token 
    def missing_token_callback(reason):
        return {"error": "missing_authorization",
                "message": reason}, 401


    @jwt.invalid_token_loader # handles malformed token 
    def invalid_token_callback(reason):
        return {"error": "invalid_token",
                "message": reason}, 422

    
    @jwt.expired_token_loader # handles expired token 
    def expired_token_callback(jwt_header, jwt_data):
        return {"error": "token_expired",
                "message": "Token has expired"}, 401


    # register blueprints: url_prefix is added in front of every route in the blueprint 
    # ie. "/login" becomes "/api/v1/auth/login"
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth") # mounts authorization routes 
    app.register_blueprint(ticket_bp, url_prefix="/api/v1/tickets") # mounts ticket routes 

    return app


if __name__ == "__main__":
    # run server (debug mode only when FLASK_DEBUG=1)
    app = create_app()
    app.run(debug=Config.DEBUG)

  