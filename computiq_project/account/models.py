from urllib.request import HTTPBasicAuthHandler
from django.db import models
from keyring import set_password
from al_ajr.models import Entity
from django.contrib.auth.models import UserManager, AbstractUser


class CustomUserManger(UserManager):
<<<<<<< HEAD
    def get_by_username(self, name):
=======
    def get_by_username(self, username):
>>>>>>> cb3791989b2f428f29fe9d9a426d0847979f3f6c
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, name, email, password, field, state):
        user = self.model(
            email=self.normalize_email(email)
        )

        user.name = name
        user.email = email
        user.set_password(password)
        user.field = field
        user.state = state
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValueError('user must have email')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def __str__(self):
<<<<<<< HEAD
        return self.name
=======
        return self.username
>>>>>>> cb3791989b2f428f29fe9d9a426d0847979f3f6c


# Create your models here.
class User(Entity, AbstractUser):

    username = models.NOT_PROVIDED
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(('email'), unique=True)
    field = models.CharField(('field'), max_length=255, choices=[
        ("FreeLancer", "FreeLancer"),
        ("User", "User")
    ])
    rating = models.DecimalField('rating', decimal_places=1,
                                 max_digits=10,
                                 null=True,
                                 blank=True,
                                 default=0)
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
        ("ميسان", "ميسان"),
        ("الديوانيه", "الديوانيه"),
        ("المثنى", "المثنى"),
        ("ذي قار", "ذي قار"),
        ("البصره", "البصره"),
    ])
    total_rating = models.DecimalField(("total rating"),
                                       max_digits=6,
                                       decimal_places=1, default=0)
    requests_accepted = models.IntegerField("number of requests", default=0)
    requests_asked = models.IntegerField("requests asked number", default=0)

    image = models.ImageField('image', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManger()

    def get_rating(self):
        return (self.total_rating / self.requests_accepted)
