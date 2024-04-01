🐍 Python module for storing user passwords in a secure way. 

- 🔒 Passwords are stored as hashes using the `SHA-256` algorithm. 
- ✅ The module provides functions for verifying passwords. 
- 🧂 All passwords are salted with a unique salt for each password using `os.urandom(32).hex()`. 

## Libraries used

- `hashlib` for hashing passwords
- `os` for generating salts
- `unittest` for testing
- `sqlmodel` for ORM, with `sqlite` as the database

## 🧪 Tests

Unit tests are available in the `db/tests` directory.

```bash
python -m unittest
```

## Install

### Requirements

```bash
pip install -r requirements.txt
```

### Database connection

Add `CONNECTION_STRING` to your environment variables. 

