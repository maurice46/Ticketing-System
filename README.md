# Ticket Management API

A simple backend for managing support tickets. People can sign up, log in, and create, view, update and delete their own tickets. Admins can see everyone's tickets.

Built with Python and Flask.

## Getting started

**1. Set up your environment** (one time only)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On Mac or Linux, activate with `source .venv/bin/activate` instead.

**2. Start the server**

```powershell
$env:FLASK_DEBUG = "1"
python main.py
```

That's it. The API is now running at `http://127.0.0.1:5000`.

> `FLASK_DEBUG = "1"` turns on development mode, which is the easiest way to run the project on your own computer. See "Going live" at the bottom if you want to run it for real.

## Try it out

Open a second terminal and run these in order. (In PowerShell, use `curl.exe`, not `curl`.)

**Create an account**

```
curl.exe -X POST http://127.0.0.1:5000/api/v1/auth/register -H "Content-Type: application/json" -d "{\"email\":\"me@example.com\",\"password\":\"secret123\"}"
```

**Log in** (you'll get back an `access_token`, so copy it)

```
curl.exe -X POST http://127.0.0.1:5000/api/v1/auth/login -H "Content-Type: application/json" -d "{\"email\":\"me@example.com\",\"password\":\"secret123\"}"
```

**Create a ticket** (paste your token where it says `<token>`)

```
curl.exe -X POST http://127.0.0.1:5000/api/v1/tickets/ -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d "{\"title\":\"Printer broken\",\"description\":\"Third floor\"}"
```

**See your tickets**

```
curl.exe http://127.0.0.1:5000/api/v1/tickets/all -H "Authorization: Bearer <token>"
```

## What you can do

Every address below starts with `/api/v1`.

| Action | Method and address | Who can do it |
|---|---|---|
| Sign up | `POST /auth/register` | anyone |
| Log in | `POST /auth/login` | anyone |
| See all users | `GET /auth/all` | admins only |
| Create a ticket | `POST /tickets/` | logged-in users |
| See your tickets | `GET /tickets/all` | logged-in users (admins see everyone's) |
| See one ticket | `GET /tickets/<id>` | the ticket's owner or an admin |
| Edit a ticket | `PATCH /tickets/<id>` | the ticket's owner or an admin |
| Delete a ticket | `DELETE /tickets/<id>` | the ticket's owner or an admin |

A ticket's status can be `open`, `in_progress` or `closed`.

## Running the tests

```
pytest -v
```

The tests use a temporary database, so they never touch your real data.

## Good to know

- Passwords must be at least 8 characters.
- Your data is saved in a file called `tickets.db` in the project folder. Delete it to start fresh.
- There's no button for making someone an admin yet. For now, change that user's `role` to `admin` directly in the database.

## Going live

When you're not in development mode, the app needs two private keys so logins stay secure. Create two with this command (run it twice):

```
python -c "import secrets; print(secrets.token_hex(32))"
```

Then set them before starting the server:

```powershell
$env:SECRET_KEY = "<first key>"
$env:JWT_SECRET_KEY = "<second key>"
python main.py
```

Keep these keys private and never share them or commit them to GitHub.