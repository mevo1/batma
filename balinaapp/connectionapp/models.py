from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Api(models.Model):
    name = models.CharField(max_length=30)
    adress = models.CharField(max_length=64)
    secretkey = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name}"

