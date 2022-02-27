from ast import Global
from http.client import PROCESSING
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router
from typing import List
from pydantic import UUID4

from common.schemas import MessageOut
from al_ajr.models import Request
from account.models import User
from al_ajr.schemas import  RequestCreate, RequestOut, RequestUpdate
from account.authorization import GlobalAuth

User = get_user_model()

request_controller = Router(tags=['Requests'])
message_controller = Router(tags=['Messges'])

"""
this endpoint get you all of the requests
"""
@request_controller.get("", response={
    200: List[RequestOut],
    400: MessageOut
})
def all_requests(request):

    requests = Request.objects.all().select_related('requester', "receiver")
    if not requests:
        return 400, {"detail": "no requests found"}
    return 200, requests


"""
gives back a specifc request by id
"""
@request_controller.get("/request/{request_id}", response=RequestOut)
def get_request(request, request_id: UUID4):
    request_ = get_object_or_404(Request, id=request_id)
    return request_


"""
creates a request
"""
@request_controller.post("/requset", auth=GlobalAuth(), response=MessageOut)
def create_request(request, payload: RequestCreate):

    user = get_object_or_404(User, id=request.auth["pk"])
    request_ = Request.objects.create(**payload.dict(),
                                        requester_id=user,
                                        status="NEW")
    return 200, {"detail": "request created successfully"}


"""
updates a specifc request by id
"""
@request_controller.put("/request/{request_id}/update", auth=GlobalAuth(), response={
    200: MessageOut,
    401: MessageOut})
def update_request(request, request_id: UUID4, payload: RequestUpdate):

    # Make sure the the requester is the one who can do changes to the request
    user = get_object_or_404(User, id=request.auth["pk"])

    requester_id = get_object_or_404(Request, id=request_id)
    requester_id = requester_id.requester

    if str(user.email) != str(requester_id):
        return 401, {"detail": "غير مصرح بالتغير"}
    
    request_ = get_object_or_404(Request, id=request_id)
    for attr, value in payload.dict().items():
        setattr(request_, attr, value)
    request_.save()
    return 200, {"detail": "تم تحديث الطلب بنجاح"}


"""
allow the free lancer to take on a request
"""
@request_controller.put("/request/{request_id}/accept", auth=GlobalAuth())
def accept_request(request, request_id: UUID4):

    user = get_object_or_404(User, id=request.auth["pk"])
    request_ = get_object_or_404(Request, id=request_id)
    request_.receiver = user
    request_.status = "PROCESSING"
    request_.save()

    return 200, {"detail": "تم قبول الطلب بنجاح"}