from email.policy import default
from django.db import models
from django.contrib.auth.models import  User
# Create your models here.
class customUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,max_length=100)
    contact = models.CharField(max_length=10)
    year = models.IntegerField()
    dept = models.CharField(max_length=20,default=None)
    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
class Events(models.Model):
    eventName = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    link = models.URLField()

    def __str__(self):
        return self.eventName