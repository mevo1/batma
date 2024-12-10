from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Indicator(models.Model):
    title = models.CharField(max_length=100)
    code = models.TextField()
    on_graph = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Coins(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

