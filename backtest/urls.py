from django.urls import path
from . import views

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/invest
# http://127.0.0.1:8000/backtest
# http://127.0.0.1:8000/account

urlpatterns = [
    path("", views.home),
    path("home", views.home, name = 'home'),
    path("backtest", views.backtest, name = 'backtest'),
    path("", views.showData, name = 'showData'),
    path("script", views.script, name = 'script' ),
    path('indicator_create', views.indicator_create, name='indicator_create'),
    path('list', views.indicator_list, name='indicator_list'),
    path('ozellikler', views.ozellikler_sayfasi, name='ozellikler'),
    path('mainmenu', views.mainmenu, name='mainmenu'),
]