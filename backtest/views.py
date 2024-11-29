from django.shortcuts import render, redirect
from .forms import MyForm, IndicatorForm
from .models import Indicator
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
import yfinance as yf

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

def strategy(request):
    return render(request, "strategy.html")

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