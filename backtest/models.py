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
    name = models.CharField(max_length=255)
    code = models.TextField()

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    strategy_count = models.IntegerField(default=0)  # Strateji sayısı
    active_bots = models.IntegerField(default=0)  # Aktif bot sayısı
    portfolio_size = models.DecimalField(max_digits=10, decimal_places=2)  # Portföy büyüklüğü

    def __str__(self):
        return self.username

class CoinList(models.Model):
    name = models.CharField(max_length = 50)
    def __str__(self):
        return self.name