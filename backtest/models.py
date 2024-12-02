from django.db import models
from django.contrib.auth.models import User

class Indicator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.TextField()
    on_graph = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Strategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    code = models.TextField()
    ilkmarj = models.IntegerField()
    emirorani = models.FloatField()
    karal = models.FloatField()
    zarardurdur = models.FloatField()
    komisyon = models.FloatField()
    islemertele = models.IntegerField()
    optlimi = models.BooleanField(default=False)
    cevapvarmi = models.BooleanField(default=False)

    def __str__(self):
        return self.name

