from decimal import Decimal
from http.client import PROCESSING
from pyexpat.errors import messages
from unicodedata import decimal
from webbrowser import get
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from ninja import Router
from typing import List
from pydantic import UUID4

from common.schemas import MessageOut
from al_ajr.models import Message, Request
from account.models import User
from al_ajr.schemas import  MessageOutClass, RequestCreate, RequestOut, RequestUpdate
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
    user.requests_asked += 1
    request_ = Request.objects.create(**payload.dict(),
                                        requester_id=user.id,
                                        status="NEW")
    user.save()
    return 200, {"detail": "request created successfully"}


"""
updates a specifc request by id
"""
@request_controller.put("/request/{request_id}/update", auth=GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut,
    401: MessageOut})
def update_request(request, request_id: UUID4, payload: RequestUpdate):

    # Make sure the the requester is the one who can do changes to the request
    user = get_object_or_404(User, id=request.auth["pk"])

    requester_id = get_object_or_404(Request, id=request_id)
    requester_id = requester_id.requester

    if str(user.email) != str(requester_id):
        return 401, {"detail": "غير مصرح بالتغير"}
    
    request_ = get_object_or_404(Request, id=request_id)

    if request_.status != "NEW":
        return 400, {"detail": "cant update a request while a freelancer is working on it"}

    for attr, value in payload.dict().items():
        setattr(request_, attr, value)
    request_.status = "EDITED"
    request_.save()
    return 200, {"detail": "تم تحديث الطلب بنجاح"}


"""
allow the free lancer to take on a request
"""
@request_controller.put("/request/{request_id}/accept", auth=GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut
})
def accept_request(request, request_id: UUID4):
    
    user = get_object_or_404(User, id=request.auth["pk"])

    if user.field != "FreeLancer":
        return 400, {"detail": "Only free lancers can take requests"}

    request_ = get_object_or_404(Request, id=request_id)
    request_.receiver = user
    request_.status = "PROCESSING"
    user.requests_accepted += 1
    user.save()
    request_.save()

    return 200, {"detail": "تم قبول الطلب بنجاح"}


@request_controller.delete("/request/{request_id}/delete", auth=GlobalAuth(),response=MessageOut)
def delete_request(request, request_id: UUID4):

    request_ = get_object_or_404(Request, id=request_id)
    request_.delete()
    return 200, {"detail": "تم حذف الطلب بنجاح"}


@request_controller.put("/request/{request_id}/finish", auth=GlobalAuth(), response={
    200: MessageOut,
    400: MessageOut
})
def finish_request(request, request_id: UUID4, rating: Decimal):

    request_ = get_object_or_404(Request, id=request_id)
    if request_.status == "DONE":
        return 400, {"detail": "cant rate an already finshed request"}
    freelancer = request_.receiver
    request_.status = "DONE"
    freelancer.total_rating += rating
    freelancer.rating=freelancer.get_rating()
    request_.save()
    freelancer.save()

    return 200, {"detail": "تم اكمال الطلب"}


@message_controller.post("/message/{receiver_id}", auth=GlobalAuth())
def send_message(request, receiver_id: UUID4, message: str):

    sender = get_object_or_404(User, id=request.auth["pk"])
    receiver = get_object_or_404(User, id=receiver_id)

    message_ = Message.objects.create(sender=sender, receiver=receiver, content=message)
    message_.save()
    return 200


@message_controller.get("/get_message/{sender_id}", auth=GlobalAuth(), response={
    200: List[MessageOutClass],
    400: MessageOut
})
def get_message(request, sender_id: UUID4):

    user = get_object_or_404(User, id=request.auth["pk"])
    sender = get_object_or_404(User, id=sender_id)
    messages = Message.objects.all().filter(sender=sender, receiver=user)
    if not messages:
        return 400, {"detail": "No messages were received"}
        
    return 200, messages
