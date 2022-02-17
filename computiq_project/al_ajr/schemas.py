import email
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Schema
from pydantic import UUID4

from account.models import User

class UUIDSchema(Schema):
    id: UUID4

class MessageOut(Schema):
    detail: str