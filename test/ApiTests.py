import unittest
from run_app import app
from src.util import const


class ApiTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.login()

    def login(self):
        login_data = {'username': 'user2', 'password': 'user2'}
        response = self.app.post('/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        self.session_cookie = response.headers.get('Set-Cookie')

    def test_login_ok(self):
        user = {'username': 'user1', 'password': 'user1'}
        response = self.app.post('/login', json=user)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('user', response.json)

    def test_login_error(self):
        user = {'username': 'usr9876', 'password': 'pswd12345'}
        response = self.app.post('/login', json=user)
        self.assertEqual(response.status_code, 404)
        self.assertIsInstance(response.json, dict)
        self.assertIn('errors', response.json)

    def test_do_math(self):
        data = {'operation': 'addition', 'param1': 2, 'param2': 2}
        response = self.app.post('/do-math', json=data, headers={'Cookie': self.session_cookie})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('result', response.json)
        self.assertEqual(response.json['result'], 4)

    def test_lack_credits(self):
        data = {'operation': 'random_string'}
        response1 = self.app.post('/do-math', json=data, headers={'Cookie': self.session_cookie})
        response2 = self.app.post('/do-math', json=data, headers={'Cookie': self.session_cookie})
        response3 = self.app.post('/do-math', json=data, headers={'Cookie': self.session_cookie})
        self.assertEqual(response3.status_code, 409)
        self.assertIn('errors', response3.json)
        self.assertIn(const.ERR_REQUESTS_LIMIT, response3.json['errors'])

    def test_my_records(self):
        data = {'page_size': 3, 'page_num': 2}
        response = self.app.post('/my-records', json=data, headers={'Cookie': self.session_cookie})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('records', response.json)
        self.assertIsInstance(response.json['records'], list)

    def test_logout(self):
        response = self.app.post('/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('message', response.json)


if __name__ == '__main__':
    unittest.main()
