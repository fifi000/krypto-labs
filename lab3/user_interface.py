from db.auth import create_user, is_unique_username, verify_password


def sign_up():
    print('Sign up form')
    print('= ' * 20)

    # Get username
    while True: 
        username = input('Username: ')
        try:
            is_valid_username(username)
        except ValueError as e:
            print(e)
            continue
        break
    
    # Get password
    while True:
        password = input('Password: ')
        try:
            is_valid_password(password)
        except ValueError as e:
            print(e)
            continue
        break

    # Reenter password 
    while True:
        reentered_password = input('Reenter password: ')
        if password == reentered_password:
            break
        print('Passwords do not match')

    try:
        create_user(username, password)
    except Exception as e:
        print(e)
        print('User could not be signed up')
        return
    
    print('User signed up successfully')    


def sign_in():
    print('Sign up form')
    print('= ' * 20)

    # Get username      
    while True: 
        username = input('Username: ')
        password = input('Password: ')
        if try_sign_in(username, password):
            print('User signed in successfully')
            return
        print('User could not be signed in\n')


def is_valid_username(username: str):
    if len(username) < 6:
        raise ValueError('Username must be at least 6 characters long')
    if len(username) > 128:
        raise ValueError('Username must be at most 128 characters long')
    if not is_unique_username(username):
        raise ValueError('Username is already taken')
    

def is_valid_password(password: str):
    if len(password) < 12:
        raise ValueError('Password must be at least 12 characters long')
    if len(password) > 1024:
        raise ValueError('Password must be at most 1024 characters long')
    

def try_sign_in(username: str, password: str):
    return verify_password(username, password)
    
