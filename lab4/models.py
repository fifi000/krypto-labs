from pydantic import BaseModel


class SymmetricKey(BaseModel):
    key: str


class AsymmetricKey(BaseModel):
    private_key: str
    public_key: str


class Message(BaseModel):
    message: str
