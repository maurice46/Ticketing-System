from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

def register_user(data):
    user = User(
        email=data["email"],
        password=generate_password_hash(data["Password"])
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "user created"}, 201

def login_user(data):
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password_hash(user.password, data["password"]):
        return {"error": "invalid credentials"}, 401
    return {"message": "login successfull"}, 200

