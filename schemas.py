from pydantic import BaseModel


class Email(BaseModel):
    subject: str
    body: str
