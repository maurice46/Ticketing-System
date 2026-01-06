from flask import Blueprint, request
from .auth_service import login_user, register_user

"""
Blueprint is used to group related routes
request to access incoming HTTP request data

auth is the blueprint identifier
__name__ helps Flask locate related resources 
"""

auth_bp = Blueprint("auth", __name__)

# define a POST endpoint under this blueprint at /register 
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return register_user(request.get_json())

# define a POST endpoint under this blueprint at /login
@auth_bp.route("/login", methods=["POST"])
def login():
    return login_user(request.get_json())


