from django.db import models

class Indicator(models.Model):
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

