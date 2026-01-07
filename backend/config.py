"""
Centralized App Settings 

Reads the environment variable SECRET_KEY.
- If it exists, its value is used.
- If it does not exist, the default string "dev-secret" is used.
- This is typically used for session signing, cryptographic operations, or app security.

Defines the database connection string for SQLAlchemy.
- Uses SQLite
- Stores data in a local file named tickets.db
- sqlite:/// means a relative path in the current working directory.

Intended to disable SQLAlchemy’s event-based change tracking (used by Flask-SQLAlchemy to reduce overhead).
However, the attribute name is misspelled (sqlachmey instead of sqlalchemy), so frameworks expecting SQLALCHEMY_TRACK_MODIFICATIONS 
will ignore this setting
"""
import os
class Config: # REQUIRES EXACT UPPERCASE NAMES 
    # used for session signing and security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    # SQLite database stored locally 
    SQLALCHEMY_DATABASE_URI = "sqlite:///tickets.db"
    # disables expensive change tracking 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # signs JWT tokens (keep in secret in production)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chage-me-in-prod")
    # token expiration (seconds)
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600")) # seconds


