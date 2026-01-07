from flask import Blueprint, request
from auth_service import login_user, register_user, list_users

"""
Define authentication 
Blueprint is used to group related routes
request to access incoming HTTP request data

auth is the blueprint identifier
__name__ helps Flask locate related resources 
"""
auth_bp = Blueprint("auth", __name__)

# define a POST endpoint under this blueprint at /register 
@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {
            "error": "Request must be JSON",
            "hint": "Set Content-Type: application/json"
        }, 415
    
    data = request.get_json(silent=True)

    return register_user(data)

# define a POST endpoint under this blueprint at /login
@auth_bp.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return {
            "error": "Request must be JSON"
        }
    data = request.get_json(silent=True)
    return login_user(data)

@auth_bp.route("/all", methods=["GET"])
def users():
    return list_users()
