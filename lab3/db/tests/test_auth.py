import unittest
from unittest.mock import patch, MagicMock

from ..auth import create_user, is_unique_username, verify_password
from ..models import UserModel  # Adjust the import path based on your project structure


class TestDBModels(unittest.TestCase):

    @patch('db.auth._session')
    def test_create_user(self, mock_session):
        """Test create_user function."""
        # Mock the session and its methods
        mock_session.return_value = MagicMock()

        # Call create_user
        create_user('testuser', 'password1234')

        # Check if session.add and session.commit were called
        session = mock_session.return_value
        session.add.assert_called()
        session.commit.assert_called()

    @patch('db.auth._session')
    def test_is_unique_username(self, mock_session):
        """Test is_unique_username function for both unique and non-unique usernames."""
        # Mock the session and its exec method for a unique username
        mock_session.return_value.exec.return_value.first.return_value = None

        # Call is_unique_username with a unique username
        self.assertTrue(is_unique_username('uniqueuser'))

        # Mock the session and its exec method for a non-unique username
        mock_session.return_value.exec.return_value.first.return_value = UserModel()

        # Call is_unique_username with a non-unique username
        self.assertFalse(is_unique_username('existinguser'))

    @patch('db.auth._session')
    def test_verify_password_correct(self, mock_session):
        """Test verify_password function with correct password."""
        # Mock the user object and its verify_password method
        mock_user = MagicMock()
        mock_user.verify_password.return_value = True

        # Mock the session and its exec method to return the mock user
        mock_session.return_value.exec.return_value.first.return_value = mock_user

        # Call verify_password with correct password
        self.assertTrue(verify_password('testuser', 'correctpassword'))

    @patch('db.auth._session')
    def test_verify_password_incorrect(self, mock_session):
        """Test verify_password function with incorrect password."""
        # Mock the user object and its verify_password method
        mock_user = MagicMock()
        mock_user.verify_password.return_value = False

        # Mock the session and its exec method to return the mock user
        mock_session.return_value.exec.return_value.first.return_value = mock_user

        # Call verify_password with incorrect password
        self.assertFalse(verify_password('testuser', 'wrongpassword'))

    @patch('db.auth._session')
    def test_verify_password_no_user(self, mock_session):
        """Test verify_password function when the user does not exist."""
        # Mock the session and its exec method to return None
        mock_session.return_value.exec.return_value.first.return_value = None

        # Call verify_password when the user does not exist
        self.assertFalse(verify_password('nonexistentuser', 'any_password'))


if __name__ == '__main__':
    unittest.main()
