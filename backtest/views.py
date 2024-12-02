from django.shortcuts import render, redirect
from .forms import MyForm, IndicatorForm
from .models import Indicator, Strategy
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
import yfinance as yf
from rest_framework import viewsets
from .serializers import StrategySerializer


coinler = ["bitcoin","ethereum","pepe"]
range = ["1 yıl", "1 ay", "1 hafta"]

def home(request):
    data = {
        "coins": coinler,
        "ranges": range
    }
    return render(request, "index.html", data)

def backtest(request):
    return render(request, "backtest.html")

def mainmenu(request):
    user = User.objects.get(username = 'bilal_bostan')
    context = {
        'user': user,
    }
    return render (request, 'mainmenu.html', context)

def strategy_page(request):
    return render(request, 'strategy.html')

class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

def leftmenu(request):
    return render(request, "leftmenu.html")

def api(request):
    return render(request, "api.html")

def workingbot(request):
    return render(request, "workingbot.html")

def sift(request):
    return render(request, "sift.html")

def community(request):
    return render(request, "community.html")

def indicator(request):
    return render(request, "indicator.html")

def logout(request):
    return render(request, "index.html")