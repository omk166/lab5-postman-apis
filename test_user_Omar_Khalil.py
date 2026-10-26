"""Lab 7 graded activity — Omar Khalil (omk166)."""
import importlib
import sqlite3

import pytest

import database


@pytest.fixture
def db_path(tmp_path, monkeypatch):
    path = tmp_path / "users.db"
    monkeypatch.setattr(database, "DATABASE", path)
    return path


@pytest.fixture
def empty_db(db_path):
    database.create_db_table()
    return db_path


@pytest.fixture
def user():
    return dict(name="Omar Khalil", email="omar@example.com", phone="70123456",
                address="Beirut", country="Lebanon")


@pytest.fixture
def saved_user(empty_db, user):
    return database.insert_user(user)


@pytest.fixture
def client(empty_db):
    import app
    app.app.config.update(TESTING=True)
    return app.app.test_client()


def read_rows(path):
    """Check persisted results independently of the functions under test."""
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute("SELECT * FROM users ORDER BY user_id")]


def test_database_created_with_initial_users_on_first_app_run(db_path):
    assert not db_path.exists()
    import app
    importlib.reload(app)
    assert db_path.is_file()
    expected = [dict(user_id=1, name="John Doe", email="jondoe@gamil.com",
                     phone="067765434567", address="John Doe Street, Innsbruck",
                     country="Austria")]
    assert read_rows(db_path) == expected
    importlib.reload(app)
    assert read_rows(db_path) == expected  # Restart must not duplicate seed users.


def test_insert_user(empty_db, user):
    inserted = database.insert_user(user)
    assert type(inserted["user_id"]) is int
    assert inserted["user_id"] > 0
    assert inserted == dict(user, user_id=inserted["user_id"])
    assert read_rows(empty_db) == [inserted]


def test_get_users(empty_db, user):
    assert database.get_users() == []
    first = database.insert_user(user)
    second = database.insert_user(dict(user, name="Second User", email="second@example.com"))
    assert database.get_users() == [first, second]


def test_get_user_by_id(saved_user):
    assert database.get_user_by_id(saved_user["user_id"]) == saved_user
    assert database.get_user_by_id(99999) is None


def test_update_user(saved_user, empty_db):
    updated = dict(saved_user, name="Updated Omar", email="updated@example.com",
                   phone="70987654", address="Tripoli", country="Lebanon")
    assert database.update_user(updated) == updated
    assert read_rows(empty_db) == [updated]


def test_delete_user(saved_user, empty_db):
    assert database.delete_user(saved_user["user_id"]) == {"status": "User deleted successfully"}
    assert read_rows(empty_db) == []


def test_api_get_user(client, saved_user):
    response = client.get(f'/api/users/{saved_user["user_id"]}')
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == saved_user


def test_api_get_users(client, saved_user):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert response.get_json() == [saved_user]


def test_api_add_user(client, user, empty_db):
    response = client.post('/api/users/add', json=user)
    assert response.status_code == 201
    data = response.get_json()
    assert type(data["user_id"]) is int
    assert data == dict(user, user_id=data["user_id"])
    assert read_rows(empty_db) == [data]


def test_api_update_user(client, saved_user, empty_db):
    updated = dict(saved_user, name="Updated Omar", email="new@example.com",
                   phone="71987654", address="Saida", country="Lebanon")
    response = client.put('/api/users/update', json=updated)
    assert response.status_code == 200
    assert response.get_json() == updated
    assert read_rows(empty_db) == [updated]


def test_api_delete_user(client, saved_user, empty_db):
    response = client.delete(f'/api/users/delete/{saved_user["user_id"]}')
    assert response.status_code == 200
    assert response.get_json() == {"status": "User deleted successfully"}
    assert read_rows(empty_db) == []
    response = client.get(f'/api/users/{saved_user["user_id"]}')
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}
