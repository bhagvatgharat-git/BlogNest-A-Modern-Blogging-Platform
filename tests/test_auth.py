import unittest
from app import create_app, db
from app.models import User
from config import TestConfig

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        user = User(username='hashman', email='hash@test.com')
        user.set_password('mysecretpass')
        self.assertTrue(user.check_password('mysecretpass'))
        self.assertFalse(user.check_password('wrongpass'))
        self.assertNotEqual(user.password_hash, 'mysecretpass')

    def test_registration_and_login_flow(self):
        # Register user
        response = self.client.post('/auth/register', data={
            'username': 'johndoe',
            'email': 'john@example.com',
            'full_name': 'John Doe',
            'password': 'SecurePassword123',
            'confirm_password': 'SecurePassword123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(username='johndoe').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.full_name, 'John Doe')

        # Log in with username
        login_resp = self.client.post('/auth/login', data={
            'login_identifier': 'johndoe',
            'password': 'SecurePassword123'
        }, follow_redirects=True)
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn(b'johndoe', login_resp.data)

        # Log out
        logout_resp = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(logout_resp.status_code, 200)
        self.assertIn(b'Log In', logout_resp.data)

    def test_prevent_duplicate_registration(self):
        user1 = User(username='uniqueuser', email='unique@example.com')
        user1.set_password('pass123')
        db.session.add(user1)
        db.session.commit()

        # Try registering with same username
        resp1 = self.client.post('/auth/register', data={
            'username': 'uniqueuser',
            'email': 'another@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'already taken', resp1.data)

        # Try registering with same email
        resp2 = self.client.post('/auth/register', data={
            'username': 'newuser2',
            'email': 'unique@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'already exists', resp2.data)

if __name__ == '__main__':
    unittest.main()
