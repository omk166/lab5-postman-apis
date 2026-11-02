import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)
DB_PATH = Path(os.environ.get("DB_PATH", "/data/users.db"))

def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        if db.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
            db.executemany("INSERT INTO users (name) VALUES (?)", [("Omar",), ("Ali",), ("Sara",)])

@app.get("/get_users")
def get_users():
    with sqlite3.connect(DB_PATH) as db:
        names = [row[0] for row in db.execute("SELECT name FROM users ORDER BY id")]
    return jsonify(names)

initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
