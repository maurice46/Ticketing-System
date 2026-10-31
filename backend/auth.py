from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth_service import login_user, register_user, list_users

"""
Blueprint is used to group related routes | request to access incoming HTTP request data
"auth" = blueprint identifier and __name__ helps Flask locate related resources 
"""

auth_bp = Blueprint("auth", __name__)

JSON_ERRORS = {
    "error": "Request must be JSON",
    "hint": "Set Content-Type: application/json"
}

# define a POST endpoint under this blueprint at /register 
@auth_bp.route("/register", methods=["POST"])
def register():
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
@jwt_required 
def users():
    user_id = int(get_jwt_identity())
    return list_users(user_id)


