from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

"""
Business Logic for Authentication:
- User registration
- User login
- Listing users
"""

def register_user(data):
    if not data or "email" not in data or "password" not in data:
        return {"error": "email and password required"}, 400 # HTTP 400 -> Bad input
    
    email = data["email"].strip().lower() # normalize email 
    password = data["password"] # extract password 

    if not email or not password:
        return {"error": "email and password required"}, 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"error": "email already registered"}, 409

    user = User(
        email=email,
        password=generate_password_hash(password) # hashes passwords to keep "secure"
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "user created", "id": user.id, "email": user.email}, 201

def login_user(data):
    if not data or "email" not in data or "password" not in data:
        return {"error": "email and password required"}, 400
    
    email = data["email"].strip().lower()
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return {"error": "invalid credentials"}, 401
    
    # identity will be stored in the token as a "sub" claim
    access_token = create_access_token(identity=str(user.id))

    return {"message": "login successfully",
            "access_token": access_token,
            "user": {"id": user.id, "email": user.email, "role": user.role}
            }, 200

def list_users():
    users = User.query.all() # fetch all users
    if not users:
        return {
            "error" : "No users"
        }, 401
    return [{"id": user.id, "email": user.email, "role": user.role} 
            for user in users]
