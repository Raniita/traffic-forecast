from pydantic import BaseModel

class Status(BaseModel):
    message: str

class HTTPUnauthorizedError(BaseModel):
    detail: str