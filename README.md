# Ticketing Management System

A RESTful API backend for creating, managing, and tracking support tickets,
built with Flask and secured with JWT authentication.

---

## Features

- User registration and login with hashed passwords
- JWT-based authentication with tokens
- Role-based access control (user / admin)
- Full ticket CRUD — create, read, update, delete
- Ownership enforcement — users can only modify their own tickets
- Versioned API endpoints (`/api/v1/`)

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Flask |
| Database | SQLite via SQLAlchemy |
| Authentication | flask-jwt-extended |
| Password hashing | Werkzeug |
| Testing | Postman |

---

## Project Structure
---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|--------|---------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and receive JWT token | No |
| GET | `/api/v1/auth/all` | List all users | No |

### Tickets

| Method | Endpoint | Description | Auth required |
|--------|---------|-------------|---------------|
| POST | `/api/v1/tickets/` | Create a ticket | Yes |
| GET | `/api/v1/tickets/all` | List all tickets | Yes |
| GET | `/api/v1/tickets/<id>` | Get a specific ticket | Yes |
| PATCH | `/api/v1/tickets/<id>` | Update a ticket | Yes |
| DELETE | `/api/v1/tickets/<id>` | Delete a ticket | Yes |

---

## Request & Response Examples

### Register
```json
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response 201:
{
  "message": "user created",
  "id": 1,
  "email": "user@example.com"
}
```

### Login
```json
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response 200:
{
  "message": "login successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

### Create a Ticket
```json
POST /api/v1/tickets/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Login page is broken",
  "description": "Users cannot log in on mobile devices."
}

Response 201:
{
  "id": 1,
  "title": "Login page is broken",
  "creator id": 1
}
```

### Update a Ticket
```json
PATCH /api/v1/tickets/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "status": "resolved"
}

Response 200:
{
  "message": "updated"
}
```

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/maurice46/ticketing-system
cd ticketing-system
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install flask flask-sqlalchemy flask-jwt-extended werkzeug
```

**4. Set environment variables (optional)**
```bash
export SECRET_KEY=your-secret-key
export JWT_SECRET_KEY=your-jwt-secret
export JWT_ACCESS_TOKEN_EXPIRES=3600
```

**5. Run the server**
```bash
python app.py
```

The server runs at `http://127.0.0.1:5000` by default.

---

## Authorization Rules

- Any authenticated user can create tickets and view all tickets
- Only the ticket creator or an admin can view, update, or delete a specific ticket
- Roles are assigned at the database level (`user` by default, `admin` manually)

---

## Known Limitations

- SQLite is used for simplicity — swap `SQLALCHEMY_DATABASE_URI` in `config.py`
  for PostgreSQL or MySQL in a production environment
- The `/api/v1/auth/all` endpoint is unprotected and should be admin-gated
  before any production deployment
- JWT secrets fall back to default values if environment variables are not set —
  always set these explicitly in production

---

## Author

Maurice Murillo · [github.com/maurice46](https://github.com/maurice46)
