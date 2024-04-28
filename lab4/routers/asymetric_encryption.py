import base64

from fastapi import APIRouter, HTTPException
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from models import AsymmetricKey, Message


router = APIRouter(
    prefix="/asymetric",
    tags=["asymetric"],
)

private_key = None
public_key = None


@router.get("/key")
def generate_asymmetric_key():
    global private_key, public_key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return {"private_key": private_key_pem.decode(), "public_key": public_key_pem.decode()}


@router.post("/key")
def set_asymmetric_key(key: AsymmetricKey):
    global private_key, public_key
    private_key = serialization.load_pem_private_key(
        key.private_key.encode(),
        password=None,
    )
    public_key = serialization.load_pem_public_key(
        key.public_key.encode(),
    )
    return {"status": "Asymmetric key set."}


@router.post("/sign")
def sign_message(message: Message):
    global private_key
    if private_key is None:
        raise HTTPException(status_code=400, detail="No private key set.")
    signature = private_key.sign(
        message.message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return {"signature": base64.b64encode(signature).decode()}


@router.post("/verify")
def verify_message(message: Message):
    global public_key
    if public_key is None:
        raise HTTPException(status_code=400, detail="No public key set.")
    signature = base64.b64decode(message.message.encode())
    try:
        public_key.verify(
            signature,
            message.message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return {"status": "Signature is valid."}
    except:
        raise HTTPException(status_code=400, detail="Signature is invalid.")