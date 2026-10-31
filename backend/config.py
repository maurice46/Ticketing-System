"""
Application Configuration
Secrects MUST come from environment variables. The app refusts to start without
them, so a forgotten variable can nenver silently fall back to a guessable key.
Local Development: set FLASK_DEBUG=1 to allow insecure built-in dev keys and to 
run the server in debug mode. 
Generate a real secret with: python -c "import secrets; print(secret.token_hex(32))"
Reads the environment variable SECRET_KEY:
- If it exists, its value is used
- If it doesn't exist, the default string "dev-secret" is used
Defines the database connection string for SQLAlchemy:
- Uses SQLite
- Stores data in a local file named tickets.db (sqlite:/// -> relative path in the current working directory)
"""
import os

MIN_SECRET_LEN = 32 # recommended keys of at least 32 bytes 

# True only if FLASK_DEBUG is "1", "true", or "yes" anything else False 
_DEBUG = os.getenv("FLASK_DEBUG", "0").strip().lower() in ("1", "true", "yes")

def _secret(name): # read a secret from the environment or fail
    value = os.getenv(name) # none if variable isn't set 

    if value:
        if len(value) < MIN_SECRET_LEN:
            raise RuntimeError(
                f"{name} is too short ({len(value)} characters)"
                f"Use at least {MIN_SECRET_LEN} characters"
            )
        return value

    # not set, but debug mode: use a throwaway key so local dev just works 
    if _DEBUG: # insecure on purpose: only reachable when FLASK_DEBUG=1
        return f"dev-only-insecure-{name.lower()}-do-not-user-in-production"

    # not set and not debug: crash at startup instead of running with a weak key
    raise RuntimeError(
        f"{name} is not set. Set it as an environment variable"
        f"(or set FLASK_DEBUG=1 for local development). Generate one with: "
        f'python -c "import secrets; print(secrets.token_hex(32))"'
    )

class Config: # Flask copies every UPPERCASE attribute here into app.config (main.py)

    # runs the dev server in debug mode only when explicitly requested 
    DEBUG = _DEBUG

    # used for session signing and security 
    SECRET_KEY = _secret("SECRET_KEY")

    # signs JWT tokens (anyone with thios key could forge logins, keep private)
    JWT_SECRET_KEY = _secret("JWT_SECRET_KEY")
    
    # SQLite by default: set DATABASE_URL to use another database 
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///tickets.db")
    
    # disables expensive change tracking 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # token expiration (in seconds); 3600 = 1 hour
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600")) 

