from pydantic import BaseModel


class Email(BaseModel):
    subject: str
    body: str


class New(BaseModel):
    name: str
    email: str
