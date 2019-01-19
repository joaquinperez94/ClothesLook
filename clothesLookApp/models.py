from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager

# Create your models here.
# class User(models.Model):
#     name=models.CharField(max_length=100)
#     nick=models.CharField(unique=True,max_length=20)
#     email=models.EmailField(blank=False)
#     password=models.CharField(max_length=50)
#
#     def __str__(self):
#         return "%s %s" % (self.name)

class User(AbstractBaseUser, PermissionsMixin):
    SEX_OPTIONS = (
        ('M', 'Man'),
        ('W', 'Woman'),
    )
    nickName = models.CharField(_('Nick Name'),unique=True, max_length=30)
    first_name = models.CharField(_('First name'),max_length=30, blank=True)
    last_name = models.CharField(_('Last name'),max_length=60, blank=True)
    year_birth = models.DateField(_('Year of Birth'),null=True)
    sex = models.CharField(_('Sex'),max_length=1, choices=SEX_OPTIONS, null=True)
    is_active = models.BooleanField(_('Is active'),default=True)
    is_staff = models.BooleanField(_('Is staf'),default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nickName'
    REQUIRED_FIELDS = []





class Category(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Clothing(models.Model):
    name=models.CharField(max_length=100)
    photo=models.CharField(max_length=200)
    size=models.CharField(max_length=10)
    brand=models.CharField(max_length=100)
    link=models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Look(models.Model):
    season_choice=(
        ('Primavera','Primavera'),
        ('Verano','Verano'),
        ('Otoño','Otoño'),
        ('Invierno','Invierno')
    )
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=300)
    season=models.CharField(max_length=100, choices=season_choice)
    #user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clothes = models.ManyToManyField(Clothing)
    def __str__(self):
        return self.title

class Comment(models.Model):
    subject=models.CharField(max_length=100)
    body=models.CharField(max_length=300)
    moment=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    look=models.ForeignKey(Look, on_delete=models.CASCADE)
    def __str__(self):
        return self.subject


