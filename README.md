# Ticket Management API

A Flask REST API with JWT authentication for creating and managing support tickets.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

(Mac/Linux: `source .venv/bin/activate`)

## Configuration

Secrets are read from environment variables. The app will not start without them.

| Variable | Required | Notes |
|---|---|---|
| `SECRET_KEY` | yes* | at least 32 characters |
| `JWT_SECRET_KEY` | yes* | at least 32 characters |
| `DATABASE_URL` | no | defaults to `sqlite:///tickets.db` |
| `JWT_ACCESS_TOKEN_EXPIRES` | no | seconds, default `3600` |
| `FLASK_DEBUG` | no | `1` = debug mode and insecure built-in dev keys |

\* not needed when `FLASK_DEBUG=1`.

Generate a secret:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

## Run

Local development (PowerShell):

```powershell
$env:FLASK_DEBUG = "1"
python main.py
```

Production-style (PowerShell):

```powershell
$env:SECRET_KEY = "<generated value>"
$env:JWT_SECRET_KEY = "<another generated value>"
python main.py
```

Mac/Linux: `FLASK_DEBUG=1 python main.py`

The server listens on `http://127.0.0.1:5000`.

## Test

```
pytest -v
```

Tests use a temporary database and their own test secrets (see `conftest.py`).

## Endpoints

All paths are under `/api/v1`.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | none | create account (password 8+ chars) |
| POST | `/auth/login` | none | returns `access_token` |
| GET | `/auth/all` | admin | list users |
| POST | `/tickets/` | user | create ticket |
| GET | `/tickets/all` | user | your tickets (admins see all) |
| GET | `/tickets/<id>` | owner/admin | get one ticket |
| PATCH | `/tickets/<id>` | owner/admin | update title, description, status |
| DELETE | `/tickets/<id>` | owner/admin | delete ticket |

Valid statuses: `open`, `in_progress`, `closed`.

## Example requests

In PowerShell use `curl.exe` (plain `curl` is an alias for something else).

```
curl.exe -X POST http://127.0.0.1:5000/api/v1/auth/register -H "Content-Type: application/json" -d "{\"email\":\"me@example.com\",\"password\":\"secret123\"}"

curl.exe -X POST http://127.0.0.1:5000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"me@example.com\",\"password\":\"secret123\"}"

curl.exe -X POST http://127.0.0.1:5000/api/v1/tickets/ -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d "{\"title\":\"Printer broken\",\"description\":\"Third floor\"}"

curl.exe http://127.0.0.1:5000/api/v1/tickets/all -H "Authorization: Bearer <access_token>"
```

## Making an admin

There is no endpoint for this yet. Set a user's `role` to `admin` directly in the database.