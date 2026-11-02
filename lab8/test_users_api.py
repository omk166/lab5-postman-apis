import importlib.util
import os
import sqlite3
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as temp:
    os.environ["DB_PATH"] = str(Path(temp) / "users.db")
    spec = importlib.util.spec_from_file_location("users_app", "users-api/app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    client = module.app.test_client()
    response = client.get("/get_users")
    assert response.status_code == 200
    assert response.get_json() == ["Omar", "Ali", "Sara"]
    with sqlite3.connect(os.environ["DB_PATH"]) as db:
        db.execute("INSERT INTO users (name) VALUES (?)", ("Database test",))
    assert client.get("/get_users").get_json()[-1] == "Database test"
    assert client.post("/get_users").status_code == 405
    print("PASS: GET returns seeded names, reflects database changes, and rejects POST.")
