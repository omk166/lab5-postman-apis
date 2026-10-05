"""Capture real HTTP responses in an isolated DB and export Postman artifacts."""
import copy
import json
import sys
import tempfile
import threading
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import database
from app import app
from werkzeug.serving import make_server

ROOT = Path(__file__).resolve().parents[1]


def main():
    original = database.DATABASE
    with tempfile.TemporaryDirectory(dir=ROOT) as directory:
        database.DATABASE = Path(directory) / 'examples.db'
        database.create_db_table()
        server = make_server('127.0.0.1', 0, app)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_port}'
        user = dict(name='John Doe', email='john@example.com', phone='067765434567',
                    address='John Doe Street, Innsbruck', country='Austria')
        items, report = [], []

        def capture(name, method, path, body=None, expected=200):
            data = json.dumps(body).encode() if body is not None else None
            req = Request(base + path, data=data, method=method,
                          headers={'Content-Type': 'application/json'} if data else {})
            with urlopen(req) as response:
                response_body = response.read().decode()
                assert response.status == expected
                status = response.status
            saved_path = path.replace('/1', '/{{user_id}}')
            saved_body = copy.deepcopy(body)
            request = {'method': method, 'header': [], 'url': '{{base_url}}' + saved_path}
            if body is not None:
                if 'user_id' in saved_body:
                    saved_body['user_id'] = '__USER_ID__'
                raw = json.dumps(saved_body, indent=2).replace('"__USER_ID__"', '{{user_id}}')
                request['header'] = [{'key': 'Content-Type', 'value': 'application/json'}]
                request['body'] = {'mode': 'raw', 'raw': raw, 'options': {'raw': {'language': 'json'}}}
            script = [f'pm.test("HTTP {expected}", () => pm.response.to.have.status({expected}));',
                      'pm.test("JSON response", () => pm.response.to.be.json);']
            if method == 'POST':
                script += ['pm.environment.set("user_id", pm.response.json().user_id);']
            if name == 'Get all users':
                script += ['pm.test("Users array contains created user", () => {',
                           '  pm.expect(pm.response.json()).to.be.an("array");',
                           '  pm.expect(pm.response.json().some(u => u.user_id === Number(pm.environment.get("user_id")))).to.be.true;', '});']
            if method == 'PUT':
                script += ['pm.test("Updated name", () => pm.expect(pm.response.json().name).to.eql("John Doe Updated"));']
            if method == 'DELETE':
                script += ['pm.test("Deleted successfully", () => pm.expect(pm.response.json().status).to.eql("User deleted successfully"));']
            items.append({'name': name, 'request': request,
                          'event': [{'listen': 'test', 'script': {'type': 'text/javascript', 'exec': script}}],
                          'response': [{'name': name + ' - successful response', 'originalRequest': copy.deepcopy(request),
                                        'status': 'Created' if status == 201 else 'OK', 'code': status,
                                        '_postman_previewlanguage': 'json',
                                        'header': [{'key': 'Content-Type', 'value': 'application/json'}],
                                        'cookie': [], 'body': json.dumps(json.loads(response_body), indent=2)}]})
            report.append({'request': name, 'method': method, 'path': path, 'status': status,
                           'response': json.loads(response_body)})
            return json.loads(response_body)

        try:
            created = capture('Add user', 'POST', '/api/users/add', user, 201)
            capture('Get all users', 'GET', '/api/users')
            capture('Get user by ID', 'GET', f'/api/users/{created["user_id"]}')
            capture('Update user', 'PUT', '/api/users/update', {**created, 'name': 'John Doe Updated'})
            capture('Delete user', 'DELETE', f'/api/users/delete/{created["user_id"]}')
            assert database.get_users() == []
        finally:
            server.shutdown()
            thread.join()
            server.server_close()
            database.DATABASE = original

    output = ROOT / 'postman'
    output.mkdir(exist_ok=True)
    collection = {'info': {'name': 'Flask user app',
                          'description': 'Lab 5 CRUD requests, actual captured examples, and automated assertions. Run in listed order.',
                          'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'}, 'item': items}
    environment = {'name': 'Flask user app - Local', 'values': [
        {'key': 'base_url', 'value': 'http://127.0.0.1:5000', 'type': 'default', 'enabled': True},
        {'key': 'user_id', 'value': '1', 'type': 'default', 'enabled': True}], '_postman_variable_scope': 'environment'}
    for name, value in [('Flask user app.postman_collection.json', collection),
                        ('Local.postman_environment.json', environment), ('http-verification.json', report)]:
        (output / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    print('Verified all 5 endpoints over HTTP; exported collection, environment, and real examples.')


if __name__ == '__main__':
    main()
