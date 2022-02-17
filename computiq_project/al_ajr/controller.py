from asyncio.proactor_events import constants
from email.message import Message
from multiprocessing.sharedctypes import Value
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4
from typing import List

from account.models import User

from al_ajr.schemas import CreateUser, MessageOut, UserOut

