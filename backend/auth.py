from flask import Blueprint, request # groups routes, holds incoming HTTP data
from flask_jwt_extended import jwt_required, get_jwt_identity # login check, who is logged in
from auth_service import login_user, register_user, list_users

# one blueprint for all auth routes: main.py mounts it at /api/v1/auth
# "auth" = blueprint identifier and __name__ helps Flask locate related resources 
auth_bp = Blueprint("auth", __name__)

JSON_ERRORS = {
    "error": "Request must be JSON",
    "hint": "Set Content-Type: application/json"
}

# define a POST endpoint under this blueprint at /register 
@auth_bp.route("/register", methods=["POST"])
def register():
    # rejects anything that isn't sent as JSON
    if not request.is_json:
        return JSON_ERRORS, 415

    data = request.get_json(silent=True)
    return register_user(data)



# define a POST endpoint under this blueprint at /login
@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return JSON_ERRORS, 415
    
    data = request.get_json(silent=True)
    return login_user(data)



# admin-only: list every user (don't want anyone to access users)
@auth_bp.route("/all", methods=["GET"])
@jwt_required()
def users():
    # the token stores the user is as a string, convert to int
    user_id = int(get_jwt_identity())
    # list_users checks the admin role and returns 403 if the user isn't one 
    return list_users(user_id)


