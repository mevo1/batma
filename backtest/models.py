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

class Entry(models.Model):
    strategy_name = models.ForeignKey(
        'Strategy', 
        on_delete=models.CASCADE, 
        related_name='entries_by_strategy_name'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strategy_name = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    code = models.ForeignKey(
        'Strategy', 
        on_delete=models.CASCADE, 
        related_name='entries_by_code')

    ilkmarj = models.IntegerField()
    emirorani = models.FloatField()
    karal = models.FloatField()
    zarardurdur = models.FloatField()
    komisyon = models.FloatField()
    islemertele = models.IntegerField()
    optlimi = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)


    def __str__(self):
        return self.username

class CryptoSymbol(models.Model):
    symbol = models.CharField(max_length=50, unique=True)  

    def __str__(self):
        return self.symbol