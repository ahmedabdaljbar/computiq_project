from django.dispatch import receiver
from django.http import Http404, request
from django.shortcuts import get_object_or_404
from ninja import Schema
from pydantic import UUID4, Field

from common.schemas import AccountOut, UUIDSchema 


class RequestCreate(Schema):
    title: str = Field(min_length=4)
    detail: str = Field(min_length=8)
    price: float = Field(gt=0)


class RequestUpdate(RequestCreate):
    pass


class RequestOut(UUIDSchema, RequestCreate):
    requester: AccountOut
    receiver: AccountOut = None
    rating: float
    status: str


class MessageOutClass(UUIDSchema):
    sender: AccountOut
    receiver: AccountOut
    content: str