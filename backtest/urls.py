from django.urls import path
from . import views

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/invest
# http://127.0.0.1:8000/backtest
# http://127.0.0.1:8000/account

urlpatterns = [
    path("", views.home),
    path("home", views.home),
    path("backtest", views.backtest),
    path("showData", views.showData),
    path("script", views.script),

]