from fastapi import APIRouter, HTTPException
from cryptography.fernet import Fernet

from models import SymmetricKey, Message


router = APIRouter(
    prefix="/symetric",
    tags=["symetric"],
)

symmetric_key = None


@router.get("/key")
def generate_symmetric_key() -> dict:
    """
    Generate a new symmetric encryption key using Fernet.
    
    Returns:
        dict: A dictionary containing the symmetric key in a readable format.
    """
    global symmetric_key
    symmetric_key = Fernet.generate_key()

    return {"key": symmetric_key.decode()}


@router.post("/key")
def set_symmetric_key(key: SymmetricKey) -> dict:
    """
    Set the symmetric encryption key for the session.
    
    Args:
        key (SymmetricKey): The symmetric key object containing the key to be set.
    
    Returns:
        dict: A dictionary indicating that the symmetric key was successfully set.
    """
    global symmetric_key
    symmetric_key = key.key.encode()

    return {"status": "Symmetric key set."}


@router.post("/encode")
def encode_message(message: Message) -> dict:
    """
    Encode a message using the currently set symmetric key.
    
    Args:
        message (Message): The message object containing the plaintext to be encoded.
    
    Raises:
        HTTPException: If the symmetric key has not been set.
    
    Returns:
        dict: A dictionary containing the encoded message.
    """
    global symmetric_key
    if symmetric_key is None:
        raise HTTPException(status_code=400, detail="Symmetric key not set.")
    
    f = Fernet(symmetric_key)
    encoded_message = f.encrypt(message.message.encode())

    return {"encoded_message": encoded_message.decode()}


@router.post("/decode")
def decode_message(message: Message) -> dict:
    """
    Decode a message using the currently set symmetric key.
    
    Args:
        message (Message): The message object containing the ciphertext to be decoded.
    
    Raises:
        HTTPException: If the symmetric key has not been set.
    
    Returns:
        dict: A dictionary containing the decoded message.
    """
    global symmetric_key
    if symmetric_key is None:
        raise HTTPException(status_code=400, detail="Symmetric key not set.")
    
    f = Fernet(symmetric_key)
    decoded_message = f.decrypt(message.message.encode())
    
    return {"decoded_message": decoded_message.decode()}