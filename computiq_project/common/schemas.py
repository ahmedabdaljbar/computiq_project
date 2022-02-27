from pydantic import EmailStr, UUID4
from ninja import Schema


class UUIDSchema(Schema):
    id: UUID4


class MessageOut(Schema):
    detail: str



class AccountOut(UUIDSchema):
    username: str
    email: EmailStr
    rating: float = None
    state: str
    field: str