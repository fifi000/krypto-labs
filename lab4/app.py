from fastapi import FastAPI

from routers import asymetric_encryption, symetric_encryption


app = FastAPI()

app.include_router(symetric_encryption.router)
app.include_router(asymetric_encryption.router)
