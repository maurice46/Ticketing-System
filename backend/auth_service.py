from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$") # makes sure its a valid email address
MAX_EMAIL_LEN = 120
MIN_PASSWORD_LEN = 8

def _read_credentials(data):
    # return (email, password, error) | error tuple = (message, status code) or None
    if not isinstance(data, dict) or "email" not in data or "password" not in data:
        return None, None, ({"error": "email and password required"}, 400)

    email, password = data['email'], data['password']

    if not isinstance(email, str) or not isinstance(password, str):
        return None, None, ({"error": "email and password must be strings"}, 400)

    email = email.strip().lower() # normalize email

    if not email or not password:
        return None, None, ({"error": "email and password required"}, 400)

    return email, password, None

def register_user(data):
    email, password, error = _read_credentials(data)

    if error: return error

    if len(email) > MAX_EMAIL_LEN or not EMAIL_RE.match(email):
        return {"error": "invalid email address"}, 400

    if len(password) < MIN_PASSWORD_LEN:
        return {"error": f"password must be at least {MIN_PASSWORD_LEN} characters"}, 400

    if User.query.filter_by(email=email).first():
        return {"error": "email already registered"}, 409

    user = User(email=email,password=generate_password_hash(password))

    # save user to the database
    db.session.add(user)
    db.session.commit()

    return {"message": "user created", "id": user.id, "email": user.email}, 201

def login_user(data):
    email, password, error = _read_credentials(data)

    if error: return error

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return {"error": "invalid credentials"}, 401
    
    # identity will be stored in the token as a "sub" claim
    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "login successfully",
        "access_token": access_token,
        "user": {"id": user.id, "email": user.email, "role": user.role}
    }, 200

def list_users(requesting_user_id):
    requester = db.session.get(User, requesting_user_id)
    if not requester or requester.role != "admin":
        return {"error": "forbidden"}, 403

    users = User.query.all() # fetch all users
    
    return [{"id": user.id, "email": user.email, "role": user.role} for user in users], 200


