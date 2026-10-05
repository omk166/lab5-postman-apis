"""Flask API using the exact routes specified in Lab 5."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from database import (
    FIELDS, create_db_table, delete_user, get_user_by_id,
    get_users, insert_user, update_user,
)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
create_db_table()


def validated_user(update=False):
    user = request.get_json()
    if not isinstance(user, dict):
        return None, "Request body must be a JSON object"
    missing = [field for field in FIELDS if not isinstance(user.get(field), str) or not user[field].strip()]
    if missing:
        return None, "Required non-empty text fields: " + ", ".join(missing)
    if update and (type(user.get("user_id")) is not int or user["user_id"] < 1):
        return None, "user_id must be a positive integer"
    return user, None


@app.errorhandler(HTTPException)
def http_error(error):
    return jsonify(error=error.description), error.code


@app.get("/api/users")
def api_get_users():
    return jsonify(get_users())


@app.get("/api/users/<int:user_id>")
def api_get_user(user_id):
    user = get_user_by_id(user_id)
    return jsonify(user) if user else (jsonify(error="User not found"), 404)


@app.post("/api/users/add")
def api_add_user():
    user, error = validated_user()
    if error:
        return jsonify(error=error), 400
    return jsonify(insert_user(user)), 201


@app.put("/api/users/update")
def api_update_user():
    user, error = validated_user(update=True)
    if error:
        return jsonify(error=error), 400
    updated = update_user(user)
    return jsonify(updated) if updated else (jsonify(error="User not found"), 404)


@app.delete("/api/users/delete/<int:user_id>")
def api_delete_user(user_id):
    message = delete_user(user_id)
    return jsonify(message) if message else (jsonify(error="User not found"), 404)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
