# Lab7-Omar-Khalil

Omar Khalil — GitHub: omk166

Based on https://github.com/omk166/lab5-postman-apis.

Install and run:

```powershell
python -m pip install -r requirements.txt
python -m pytest -v
```

`test_user_Omar_Khalil.py` covers all ten graded requirements: database creation and initial users, insert, list, lookup by ID, update, delete, and the four single-user API operations. It also tests the list API. API tests assert status codes, complete JSON responses, and persisted database changes. Fixtures give each test an isolated temporary database.

The original Lab 5 app created an empty table. For the first-run requirement, the app now initializes the table with the John Doe sample from the Lab 5 handout (including its original email spelling). No other initial-user list was specified in the supplied handouts. Existing tables are preserved, and restarting does not duplicate users. `create_db_table()` still creates an empty table for isolated CRUD tests.

`get_user_by_id` is the actual Lab 5 function corresponding to the handout's `Get_users_by_id` item. API creation returns 201, matching this repository's existing contract.

`evidence/pytest-output.txt` contains actual captured test output. The PNG is a rendering of that output. The suite includes the four existing Lab 5 tests: 15 tests total.
