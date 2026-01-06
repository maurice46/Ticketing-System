from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

def register_user(data):
    if not data or "email" not in data or "password" not in data:
        return {"error": "emial and password required"}, 400
    user = User(
        email=data["email"],
        password=generate_password_hash(data["password"])
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "user created"}, 201

def login_user(data):
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return {"error": "invalid credentials"}, 401
    return {"message": "login successfull"}, 200

def list_users():
    users = User.query.all()
    if not users:
        return {
            "error" : "No users"
        }
    return [{"id": user.id, "email": user.email, "role": user.role} 
            for user in users]
