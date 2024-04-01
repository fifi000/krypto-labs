import unittest

from ..models import UserModel



class TestUserModel(unittest.TestCase):

    def setUp(self):
        """Create a user model instance before each test."""
        self.user = UserModel(username='testuser', hashed_password='', salt='')

    def test_set_password_length(self):
        """Test set_password raises ValueError for short passwords."""
        with self.assertRaises(ValueError):
            self.user.set_password('short')

    def test_password_hashing(self):
        """Test if the password is correctly hashed and stored."""
        password = 'securepassword123'
        self.user.set_password(password)
        self.assertNotEqual(self.user.hashed_password, password)
        self.assertTrue(self.user.hashed_password)

    def test_verify_password(self):
        """Test verify_password method for correct and incorrect passwords."""
        password = 'correctpassword'
        wrong_password = 'wrongpassword'
        self.user.set_password(password)

        # Correct password
        self.assertTrue(self.user.verify_password(password))

        # Incorrect password
        self.assertFalse(self.user.verify_password(wrong_password))


if __name__ == '__main__':
    unittest.main()
