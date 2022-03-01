from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4
from account.authorization import GlobalAuth, get_tokens_for_user
from account.schemas import AccountCreate, AuthOut, SigninSchema
from django.contrib.auth import get_user_model, authenticate
from common.schemas import MessageOut, AccountOut

User = get_user_model()

log_controller = Router(tags=['log'])


@log_controller.post('singup', response={
    400: MessageOut,
    201: AuthOut,
})
def signup(request, signup_payload: AccountCreate):
    if signup_payload.password1 != signup_payload.password2:
        return 400, {'detail': 'passwords dont match'}

    if not signup_payload.check():
        if not signup_payload.unique_check():
            user = User.objects.create_user(
                name=signup_payload.name,
                email=signup_payload.email,
                password=signup_payload.password1,
                field=signup_payload.field,
                state=signup_payload.state
            )
        else:
            return signup_payload.unique_check()
    else:
        return signup_payload.check()

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
    user = authenticate(email=signin_payload.email,
                        password=signin_payload.password)

    if not user:
        return 404, {'detail': 'user does not exist'}

    token = get_tokens_for_user(user)

    return {
        'token': token,
        'account': user
    }


@log_controller.get('', auth=GlobalAuth(), response=AccountOut)
def me(request):
    return get_object_or_404(User, id=request.auth['pk'])


@log_controller.get("/user/{user_id}", auth=GlobalAuth(), response={
    200: AccountOut,
    400: MessageOut
})
def get_user(request, user_id: UUID4):
    id_user = get_object_or_404(User, id=user_id)

    return 200, id_user