from rest_framework import serializers
from .models import Strategy

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'name', 'code']
