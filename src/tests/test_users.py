import json
from src.api.models import User
from src import db

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "john", "email": "john@algonquincollege.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "john@algonquincollege.com was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "john", "email": "john@algonquincollege.com"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "john", "email": "john@algonquincollege.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database):
    user = User(username="jeffrey", email="jeffrey@testdriven.io")
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@testdriven.io" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]

def test_all_users(test_app, test_database, add_user):
   test_database.session.query(User).delete()  # new
   add_user("john", " john@algonquincollege.com")
   add_user("fletcher", "fletcher@notreal.com")
   client = test_app.test_client()
   resp = client.get("/users")
   data = json.loads(resp.data.decode())
   assert resp.status_code == 200
   assert len(data) == 2
   assert "john" in data[0]["username"]
   assert "john@algonquincollege.com" in data[0]["email"]
   assert "fletcher" in data[1]["username"]
   assert "fletcher@notreal.com" in data[1]["email"]

def test_delete_user(test_app, test_database):
    user = User(username="jeffreyDelete", email="jeffreyDelete@testdriven.io")
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.delete(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert f"User {user.id} successfully deleted." in data["message"]

def test_update_user(test_app, test_database):
    user = User(username="jeffreyToBeUpdated", email="jeffreyToBeUpdated@testdriven.io")
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "jeffreyUpdated", "email": "jeffreyUpdated@algonquincollege.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert f"User {user.id} successfully updated." in data["message"]