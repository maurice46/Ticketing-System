"""
Test suite for the Ticketing Management System.

***CREATED WITH AI***

Part 1 (TestWorking)  -> behaviour that should work today.
Part 2 (TestDesired)  -> behaviour a solid API *should* have. Failures here point at real improvements to make.

To run: pytest -v
"""
import pytest
from config import Config


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # Use a throwaway database per test so tickets.db is never touched
    monkeypatch.setattr(Config, "SQLALCHEMY_DATABASE_URI", f"sqlite:///{tmp_path/'test.db'}")
    from main import create_app
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


BASE = "/api/v1"


def register(client, email="a@test.com", password="pw123456"):
    return client.post(f"{BASE}/auth/register", json={"email": email, "password": password})


def login(client, email="a@test.com", password="pw123456"):
    return client.post(f"{BASE}/auth/login", json={"email": email, "password": password})


def auth_header(client, email="a@test.com", password="pw123456"):
    register(client, email, password)
    token = login(client, email, password).get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def make_admin(client, email):
    from models import db, User
    with client.application.app_context():
        u = User.query.filter_by(email=email).first()
        u.role = "admin"
        db.session.commit()


# --------------------------------------------------------------------------
# Part 1: things that should already work
# --------------------------------------------------------------------------
class TestWorking:
    def test_register_success(self, client):
        r = register(client)
        assert r.status_code == 201
        assert r.get_json()["email"] == "a@test.com"

    def test_register_normalizes_email(self, client):
        register(client, "  MiXed@Test.com ")
        assert register(client, "mixed@test.com").status_code == 409

    def test_register_duplicate(self, client):
        register(client)
        assert register(client).status_code == 409

    def test_register_missing_fields(self, client):
        r = client.post(f"{BASE}/auth/register", json={"email": "x@test.com"})
        assert r.status_code == 400

    def test_register_requires_json(self, client):
        r = client.post(f"{BASE}/auth/register", data="nope")
        assert r.status_code == 415

    def test_login_success(self, client):
        register(client)
        r = login(client)
        assert r.status_code == 200
        assert "access_token" in r.get_json()

    def test_login_wrong_password(self, client):
        register(client)
        assert login(client, password="wrong").status_code == 401

    def test_login_unknown_user(self, client):
        assert login(client, "ghost@test.com").status_code == 401

    def test_ticket_requires_token(self, client):
        assert client.get(f"{BASE}/tickets/all").status_code == 401

    def test_ticket_bad_token(self, client):
        r = client.get(f"{BASE}/tickets/all", headers={"Authorization": "Bearer garbage"})
        assert r.status_code == 422

    def test_create_and_get_ticket(self, client):
        h = auth_header(client)
        r = client.post(f"{BASE}/tickets/", json={"title": "Bug", "description": "broken"}, headers=h)
        assert r.status_code == 201
        tid = r.get_json()["id"]
        g = client.get(f"{BASE}/tickets/{tid}", headers=h)
        assert g.status_code == 200
        assert g.get_json()["title"] == "Bug"

    def test_create_ticket_requires_title(self, client):
        h = auth_header(client)
        r = client.post(f"{BASE}/tickets/", json={"description": "x"}, headers=h)
        assert r.status_code == 400

    def test_get_missing_ticket(self, client):
        h = auth_header(client)
        assert client.get(f"{BASE}/tickets/999", headers=h).status_code == 404

    def test_other_user_cannot_read_update_delete(self, client):
        h1 = auth_header(client, "one@test.com")
        h2 = auth_header(client, "two@test.com")
        tid = client.post(f"{BASE}/tickets/", json={"title": "Mine"}, headers=h1).get_json()["id"]
        assert client.get(f"{BASE}/tickets/{tid}", headers=h2).status_code == 403
        assert client.patch(f"{BASE}/tickets/{tid}", json={"title": "x"}, headers=h2).status_code == 403
        assert client.delete(f"{BASE}/tickets/{tid}", headers=h2).status_code == 403

    def test_admin_can_access_any_ticket(self, client):
        h1 = auth_header(client, "one@test.com")
        h2 = auth_header(client, "admin@test.com")
        make_admin(client, "admin@test.com")
        tid = client.post(f"{BASE}/tickets/", json={"title": "Mine"}, headers=h1).get_json()["id"]
        assert client.get(f"{BASE}/tickets/{tid}", headers=h2).status_code == 200

    def test_owner_update_and_delete(self, client):
        h = auth_header(client)
        tid = client.post(f"{BASE}/tickets/", json={"title": "T"}, headers=h).get_json()["id"]
        assert client.patch(f"{BASE}/tickets/{tid}", json={"status": "closed"}, headers=h).status_code == 200
        assert client.get(f"{BASE}/tickets/{tid}", headers=h).get_json()["status"] == "closed"
        assert client.delete(f"{BASE}/tickets/{tid}", headers=h).status_code == 204
        assert client.get(f"{BASE}/tickets/{tid}", headers=h).status_code == 404


# --------------------------------------------------------------------------
# Part 2: behaviour a robust API should have (failures = to-do list)
# --------------------------------------------------------------------------
class TestDesired:
    def test_login_non_json_returns_415(self, client):
        r = client.post(f"{BASE}/auth/login", data="nope")
        assert r.status_code == 415

    def test_user_list_requires_auth(self, client):
        register(client)
        assert client.get(f"{BASE}/auth/all").status_code in (401, 403)

    def test_admin_can_list_users(self, client):
        h = auth_header(client)
        make_admin(client, "a@test.com")
        r = client.get(f"{BASE}/auth/all", headers=h)
        assert r.status_code == 200
        assert "password" not in r.get_json()[0]

    def test_non_string_email_is_400_not_500(self, client):
        r = client.post(f"{BASE}/auth/register", json={"email": 123, "password": "pw123456"})
        assert r.status_code == 400

    def test_invalid_email_rejected(self, client):
        assert register(client, "not-an-email").status_code == 400

    def test_weak_password_rejected(self, client):
        assert register(client, password="1").status_code == 400

    def test_password_hash_fits_column(self, client):
        register(client)
        from models import User
        with client.application.app_context():
            u = User.query.first()
            limit = User.password.type.length
            assert len(u.password) <= limit, f"hash is {len(u.password)} chars; column is String({limit})"

    def test_patch_without_body_is_400_not_500(self, client):
        h = auth_header(client)
        tid = client.post(f"{BASE}/tickets/", json={"title": "T"}, headers=h).get_json()["id"]
        r = client.patch(f"{BASE}/tickets/{tid}", data="", content_type="application/json", headers=h)
        assert r.status_code == 400

    def test_blank_title_rejected(self, client):
        h = auth_header(client)
        r = client.post(f"{BASE}/tickets/", json={"title": "   "}, headers=h)
        assert r.status_code == 400

    def test_invalid_status_rejected(self, client):
        h = auth_header(client)
        tid = client.post(f"{BASE}/tickets/", json={"title": "T"}, headers=h).get_json()["id"]
        r = client.patch(f"{BASE}/tickets/{tid}", json={"status": "banana"}, headers=h)
        assert r.status_code == 400

    def test_users_only_see_their_own_tickets_in_list(self, client):
        h1 = auth_header(client, "one@test.com")
        h2 = auth_header(client, "two@test.com")
        client.post(f"{BASE}/tickets/", json={"title": "private"}, headers=h1)
        listed = client.get(f"{BASE}/tickets/all", headers=h2).get_json()
        assert listed == []

    def test_create_response_key_is_snake_case(self, client):
        h = auth_header(client)
        body = client.post(f"{BASE}/tickets/", json={"title": "T"}, headers=h).get_json()
        assert "creator_id" in body

    def test_title_longer_than_column_rejected(self, client):
        h = auth_header(client)
        r = client.post(f"{BASE}/tickets/", json={"title": "x" * 500}, headers=h)
        assert r.status_code == 400

    