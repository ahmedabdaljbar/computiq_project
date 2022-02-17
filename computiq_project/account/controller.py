from dataclasses import field
import email
from os import stat
from ninja import Router
from account.authorization import get_tokens_for_user
from account.schemas import AccountCreate, AuthOut, SigninSchema
from django.contrib.auth import get_user_model, authenticate
from al_ajr.schemas import MessageOut

User = get_user_model()

log_controller = Router(tags=['log'])


@log_controller.post('singup', response={
    400: MessageOut,
    201: AuthOut,
})
def signup(request, signnup_payload: AccountCreate):
    if signnup_payload.password1 != signnup_payload.password2:
        return 400, {'detail': 'passwords dont match'}
    
    if not signnup_payload.check():
        if not signnup_payload.unique_check():
            user = User.objects.create_user(
                username= signnup_payload.username,
                email=signnup_payload.email,
                password=signnup_payload.password1,
                field=signnup_payload.field,
                state=signnup_payload.state
            )
        else:
            return signnup_payload.unique_check()
    else:
        return signnup_payload.check()

    token = get_tokens_for_user(user)

    return 201, {
        'token': token,
        'account': user
    }


@log_controller.post('signin', response={
    200: AuthOut,
    404: MessageOut
})
def signin(request, signin_payload: SigninSchema):
    user = authenticate(email=signin_payload.email, password=signin_payload.password)

    if not user:
        return 404, {'detail': 'user does not exist'}
    
    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user
    }