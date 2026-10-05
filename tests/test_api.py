"""Verify CRUD, validation, persistence, and parameterized SQL in a temporary DB."""
import tempfile
import unittest
from pathlib import Path

import database
from app import app


class UserAPITest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])
        self.original = database.DATABASE
        database.DATABASE = Path(self.temp.name) / "test.db"
        database.create_db_table()
        app.config["TESTING"] = True
        self.client = app.test_client()
        self.user = dict(name="John Doe", email="john@example.com", phone="067765434567",
                         address="John Doe Street, Innsbruck", country="Austria")

    def tearDown(self):
        database.DATABASE = self.original
        self.temp.cleanup()

    def test_crud_and_persistence(self):
        self.assertEqual(self.client.get('/api/users').json, [])
        response = self.client.post('/api/users/add', json=self.user)
        self.assertEqual(response.status_code, 201)
        user = response.json
        uid = user['user_id']
        self.assertEqual(database.get_user_by_id(uid), user)
        self.assertEqual(self.client.get(f'/api/users/{uid}').json, user)
        self.assertEqual(self.client.get('/api/users').json, [user])
        user['name'] = "Updated User"
        self.assertEqual(self.client.put('/api/users/update', json=user).json, user)
        self.assertEqual(self.client.delete(f'/api/users/delete/{uid}').status_code, 200)
        self.assertEqual(self.client.get(f'/api/users/{uid}').status_code, 404)
        self.assertEqual(self.client.get('/api/users').json, [])

    def test_invalid_requests(self):
        for value in ({}, [], None, {**self.user, 'name': ' '}):
            self.assertEqual(self.client.post('/api/users/add', json=value).status_code, 400 if value is not None else 415)
        self.assertEqual(self.client.post('/api/users/add', data='{', content_type='application/json').status_code, 400)
        for uid in (True, 0, '1'):
            self.assertEqual(self.client.put('/api/users/update', json={**self.user, 'user_id': uid}).status_code, 400)

    def test_missing_users(self):
        self.assertEqual(self.client.get('/api/users/999').status_code, 404)
        self.assertEqual(self.client.delete('/api/users/delete/999').status_code, 404)
        self.assertEqual(self.client.put('/api/users/update', json={**self.user, 'user_id': 999}).status_code, 404)

    def test_sql_text_and_cors(self):
        self.user['name'] = "Robert'); DROP TABLE users;--"
        response = self.client.post('/api/users/add', json=self.user, headers={'Origin': 'http://localhost:3000'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], self.user['name'])
        self.assertEqual(len(database.get_users()), 1)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'http://localhost:3000')


if __name__ == '__main__':
    unittest.main()
