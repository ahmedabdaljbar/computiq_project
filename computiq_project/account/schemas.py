from turtle import st
from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Schema
from al_ajr.schemas import UUIDSchema
from django.contrib.auth import get_user_model
from pydantic import EmailStr, Field

User = get_user_model()

class AccountCreate(Schema):
    username: str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str
    state: str
    field: str
    
    def check(self):
        if not self.username:
            return 400, {"detail": "Please enter your username"}
        elif not self.email:
            return 400, {"detail": "Please enter your email"}
        elif not self.field:
            return 400, {"detail": "Please chose your field"}
        elif not self.state:
            return 400, {"detail": "Please chose your state"}


    def unique_check(self):
        """
        If the name does not exist then it will check for 
        the email if it's already exists
        """
        try:
            user_buffer = get_object_or_404(User, username=self.username)
            return 400, {"detail": "username already used"}
        except Http404:
            try:
                email_buffer = get_object_or_404(User, email=self.email)
                return 400, {"detail": "email already used"}
            except Http404:
                return None


class AccountOut(UUIDSchema):
    username: str
    email: EmailStr
    state: str
    field: str


class TokenOut(Schema):
    access: str


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut


class SigninSchema(Schema):
    email: EmailStr
    password: str


class AccountUpdate(Schema):
    username: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password1: str
    new_password2: str