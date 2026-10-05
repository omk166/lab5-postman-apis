# Lab 5 — Postman and APIs

A Flask REST API that creates, reads, updates, and deletes users in SQLite, with the endpoints required by the lab handout.

## Run on Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

The app automatically creates `database.db` and the `users` table. SQLite is included in Python; no separate `db-sqlite3` package is needed. The server runs at `http://127.0.0.1:5000`. Stop it with Ctrl+C.

## Endpoints

| Method | Endpoint | Result |
| --- | --- | --- |
| GET | `/api/users` | All users, 200 |
| GET | `/api/users/<user_id>` | One user, 200 |
| POST | `/api/users/add` | Created user with generated ID, 201 |
| PUT | `/api/users/update` | Updated user, 200 |
| DELETE | `/api/users/delete/<user_id>` | Success message, 200 |

POST requires a JSON object with non-empty strings for `name`, `email`, `phone`, `address`, and `country`. PUT requires the same fields plus an integer `user_id`. Unknown users return JSON errors with 404. Invalid fields return 400; requests without a JSON content type return 415.

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "067765434567",
  "address": "John Doe Street, Innsbruck",
  "country": "Austria"
}
```

With the server running, open `http://127.0.0.1:5000/api/users` in a browser to view the list. After adding a user, open `/api/users/1` (or the returned ID) to view that user.

## Postman graded exercise

1. Create a workspace in Postman and import both JSON files from `postman`: the collection and environment.
2. Select **Flask user app - Local** as the active environment.
3. Start the Flask server and run the **Flask user app** collection in its listed order: Add user → Get all users → Get user by ID → Update user → Delete user.
4. The Add request automatically saves the generated `user_id` to the environment. Every URL uses `{{base_url}}`; the environment stores `http://127.0.0.1:5000`.
5. Each request includes a saved successful example captured from an actual local HTTP response. Expand a request to view its example. To save a fresh response from your own run, use **Save Response → Save as example**.
6. Retain the exported collection and environment as the graded deliverables. If the instructor asks for screenshots, capture your own Postman run results.

Saved examples show one captured run and its ID; live requests use the current environment ID. Running the collection creates then deletes its test user without removing other users.

The handout names the collection with a duplicated trailing “Flask”; the collection uses the intended name **Flask user app**.

Reference tutorials: [Postman quick start](https://learning.postman.com/docs/getting-started/quick-start/) and [sending requests](https://learning.postman.com/docs/use/send-requests/requests/).

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tools\build_postman.py
```

The tests cover CRUD and persistence, invalid payloads, nonexistent users, SQL-like input stored safely, and CORS. The export tool starts an isolated local HTTP server with a temporary database, exercises every required endpoint, saves actual examples, and verifies that deletion leaves its temporary database empty. Its response evidence is in `postman/http-verification.json`. It leaves your normal database untouched.

## Git workflow

The local repository contains a database implementation commit on `main`, an API/Postman implementation commit on `rest-api`, and a merge commit into `main`. The `rest-api` branch is retained for inspection. Generated databases and the virtual environment are ignored.

Postman workspace import and visual browser checks require the desktop apps; exported files and HTTP verification do not claim those UI steps were performed.
