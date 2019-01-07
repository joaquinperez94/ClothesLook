from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
#     name=models.CharField(max_length=100)
#     nick=models.CharField(unique=True,max_length=20)
#     email=models.EmailField(blank=False)
#     password=models.CharField(max_length=50)
#
#     def __str__(self):
#         return "%s %s" % (self.name)

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
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(models.Model):
    subject=models.CharField(max_length=100)
    body=models.CharField(max_length=300)
    moment=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    look=models.ForeignKey(Look, on_delete=models.CASCADE)
    def __str__(self):
        return self.subject

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
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


