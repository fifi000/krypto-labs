import unittest

from ..models import get_hasher


class TestGetHasher(unittest.TestCase):

    def test_hasher_output_type(self):
        """Test that the hasher returns bytes."""
        result = get_hasher('password123', 'abcd1234abcd1234')
        self.assertIsInstance(result, bytes)

    def test_hasher_output_length(self):
        """Test that the hasher output has a correct length."""
        result = get_hasher('password123', 'abcd1234abcd1234')
        self.assertEqual(len(result.hex()), 64)  # Since SHA-256 produces a 256-bit hash.


if __name__ == '__main__':
    unittest.main()
