# Lab 8 ? Docker and containers

**Omar Khali ? omk166**

Graded Activity 1: actual command screenshots and explanations are in
`Lab8-Omar-Khali.docx`, with original evidence in `evidence/`.

Graded Activity 2: two built and tested Docker images:

| Image | Application | Host endpoint |
| --- | --- | --- |
| `omk166/lab8-omar_khali:0.0.1-RELEASE` | Existing Lab 5 user CRUD API | `http://127.0.0.1:5000/api/users` |
| `omk166/lab8-omar_khali:0.0.2-RELEASE` | SQLite-backed names API | `http://127.0.0.2:3000/get_users` |

## Run

```powershell
docker compose up --build -d
python verify_live.py
```

Port 3000 was already occupied on 127.0.0.1 on this computer. The names API
uses 127.0.0.2:3000, retaining the required port without stopping that service.
On a computer with a free port, `3000:3000` can replace that binding.

The second API returns `["Omar", "Ali", "Sara"]` from its SQLite users table.
The database is seeded on first start and stored in a named Docker volume.

## Check the commands

```powershell
docker ps -a
docker stop lab8-users-1
docker logs lab8-users-1
docker start lab8-users-1
```

`docker ps -a` lists running and stopped containers. `docker stop` requests
that the specified container stop, escalating to a forced kill after its
shutdown timeout if necessary. `docker logs` shows the container's standard
output and error. Stop/logs accept a container name or ID; the handout's
`<image_name>` placeholder should be replaced with the container name.

Screenshots use a lab-container filter and formatted columns for readability,
and a five-line log tail. Full unformatted lab output is also supplied as text.

## Image naming

Docker repository names must be lowercase. A tag cannot include an extra
colon, so the handout's `0.0.1:RELEASE` and `0.0.2:RELEASE` are represented
as valid tags `0.0.1-RELEASE` and `0.0.2-RELEASE`.

## Source and verification

`lab5-app/app.py`, `database.py`, and `requirements.txt` come from
https://github.com/omk166/lab5-postman-apis (main). The app binds to 0.0.0.0
so that Docker port publishing works. SQLite is stored under `/data`.
The original API routes and validation are retained.

Verified both live APIs, all five Lab 5 CRUD operations, and a database
mutation test proving the names API reads its database rather than a
hardcoded response. Temporary CRUD test data is removed by the test.

```powershell
docker run --rm -v "${PWD}:/work" -w /work omk166/lab8-omar_khali:0.0.2-RELEASE python test_users_api.py
```

The screenshots were captured directly from Docker Desktop on 2 November 2026.
Images were built locally; publishing to Docker Hub was not required.

The repository link for submitting this lab is in `submission.txt`.
