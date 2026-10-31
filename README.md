# Ticket Management System

A backend API I built with Python and Flask for managing support tickets. Users create an account, log in, and keep track of their own tickets. Admins can see everything.

## What it does

- **Accounts:** people can sign up and log in
- **Tickets:** logged-in users can create, view, edit and delete tickets
- **Statuses:** every ticket is `open`, `in_progress` or `closed`
- **Privacy:** you can only see and change your own tickets
- **Admins:** admins can see every ticket and the full user list

## What I built into it

**Secure logins**
- Passwords are scrambled (hashed) before being saved, so the real password is never stored
- Logging in gives you a token that proves who you are, and it expires after an hour
- The secret keys that protect those tokens come from outside the code, and the app won't start without them

**Careful about bad input**
- Checks that emails look real and passwords are at least 8 characters
- Rejects empty or oversized ticket titles and made-up statuses
- Returns clear error messages instead of crashing

**Clean organization**
- Each part of the project has one job, which makes it easy to find things and change them

**Tested**
- 29 automated tests check that everything works, including that people can't open each other's tickets

## How it's organized

| File | What it does |
|---|---|
| `main.py` | starts the app and connects everything |
| `config.py` | settings and secret keys |
| `models.py` | the database tables (users and tickets) |
| `auth.py` | the sign up and log in addresses |
| `auth_service.py` | the rules behind sign up and log in |
| `ticket.py` | the ticket addresses |
| `ticket_service.py` | the rules behind tickets |
| `test_api.py` | the automated tests |

## Trying it yourself

```powershell
pip install -r requirements.txt
$env:FLASK_DEBUG = "1"
python main.py
```

The app now runs at `http://127.0.0.1:5000`. To run the tests, use `pytest -v`.

## What's next

- Show when each ticket was created and last changed
- Split long ticket lists into pages
- Filter tickets by status
- A simple way to make someone an admin
