import requests


base = 'http://localhost:5000'


def test_mine():
    print("Testing mining new block...")
    response = requests.get(f'{base}/mine')
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json())


def test_new_transaction():
    print("Testing creating a new transaction...")
    transaction = {
        'sender': 'address1',
        'recipient': 'address2',
        'amount': 50
    }
    response = requests.post(f'{base}/transactions/new', json=transaction)
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json())


def test_full_chain():
    print("Testing retrieving the blockchain...")
    response = requests.get(f'{base}/chain')
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json())


if __name__ == '__main__':
    test_new_transaction()  # Test creating a transaction
    test_mine()             # Test mining a new block, which includes the transaction
    test_full_chain()       # Test retrieving the full blockchain to see the results

