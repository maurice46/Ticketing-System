"""
Reads the environment variable SECRET_KEY:
- If it exists, its value is used
- If it doesn't exist, the default string "dev-secret" is used

Defines the database connection string for SQLAlchemy:
- Uses SQLite
- Stores data in a local file named tickets.db (sqlite:/// -> relative path in the current working directory)
"""
import os

class Config:
    # used for session signing and security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    
    # SQLite database stored locally 
    SQLALCHEMY_DATABASE_URI = "sqlite:///tickets.db"
    
    # disables expensive change tracking 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # signs JWT tokens (keep in secret in production)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chage-me-in-prod")
    
    # token expiration (in seconds)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600")) 


