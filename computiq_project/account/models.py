from urllib.request import HTTPBasicAuthHandler
from django.db import models
from keyring import set_password
from al_ajr.models import Entity
from django.contrib.auth.models import UserManager, AbstractUser
import uuid


class CustomUserManger(UserManager):
    def get_by_username(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


    def create_user(self, username, email, password, field, state):
        user = self.model(
            email = self.normalize_email(email)
        )

        user.username = username
        user.email = email
        user.set_password(password)
        user.field = field
        user.state = state
        user.save(using=self._db)

        return user


    def __str__(self):
        return self.username
    

# Create your models here.
class User(Entity, AbstractUser):

    username = models.CharField(("name"), max_length=50, unique=True)
    email = models.EmailField(('email'), unique=True)
    field = models.CharField(('field'), max_length=50)
    rating = models.DecimalField('rating', decimal_places=1, max_digits=10, null=True, blank=True)
    state = models.CharField('states', max_length=255, choices=[
        ("دهوك", "دهوك"),
        ("اربيل", "اربيل"),
        ("نينوى", "نينوى"),
        ("السليمانية", "السليمانية"),
        ("كركوك", "كركوك"),
        ("صلاح الدين", "صلاح الدين"),
        ("ديالى", "ديالى"),
        ("بغداد", "بغداد"),
        ("الانبار", "الانبار"),
        ("واسط", "واسط"),
        ("بابل", "بابل"),
        ("النجف", "النجف"),
        ("كربلاء", "كربلاء"),
        ("ميسان" , "ميسان"),
        ("الديوانيه", "الديوانيه"),
        ("المثنى", "المثنى"),
        ("ذي قار", "ذي قار"),
        ("البصره", "البصره"),
    ])
    # TODO get the width * height from the frontend
    image = models.ImageField('image', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManger()


    # A property that get the avg rating of all the requests that the user
    # have done
    # TODO link the user table with the quests table and bases on that relation get the rating
    # @property
    def get_rating(self):
        for i in range(4):
            print(i)