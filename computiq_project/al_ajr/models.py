from django.db import models
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Entity(models.Model):
    """
    A inhertance model to kill the duplecations in the code
    """
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True) 


class Request(Entity):
    """
    A request model to store the request that are made between
    custemers and freelancers
    """
    requester = models.ForeignKey("account.User", verbose_name="custmer_id",
                                     on_delete=models.CASCADE,
                                     related_name='requester_id')
    receiver = models.ForeignKey("account.User", verbose_name="freelancer_id",
                                     on_delete=models.CASCADE,
                                     related_name='receiver_id',
                                     blank=True,
                                     null=True)
    price = models.DecimalField('price', decimal_places=3, max_digits=10)
    title = models.CharField(('title'), max_length=100)
    detail = models.CharField('details', max_length=2000)
    status = models.CharField("status", max_length=255, choices=[
        ("NEW", "NEW"),
        ("PROCESSING", "PROCESSING"),
        ("DONE", "DONE"),
        ("DELETED", "DELETED"),
        ("EDITED", "EDITED")
    ])


class Skill(Entity):

    # Not totaly sure if this would be choices or just...
    users = models.ManyToManyField("account.User", verbose_name=("users"))
    name = models.CharField('skill name', max_length=255)
    detail = models.CharField('detail', max_length=2000)


class Message(Entity):
    sender = models.ForeignKey("account.User", verbose_name=("sender"), related_name="sender",
                               on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey("account.User", verbose_name=("receiver"), related_name="receiver",
                                  on_delete=models.DO_NOTHING)
    content = models.CharField('message', max_length=255)