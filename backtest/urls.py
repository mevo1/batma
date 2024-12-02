from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StrategyViewSet, strategy_page
from . import views

router = DefaultRouter()
router.register(r'strategies', StrategyViewSet)

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/invest
# http://127.0.0.1:8000/backtest
# http://127.0.0.1:8000/account

urlpatterns = [
    #api
    path('api/', include(router.urls)),
    #----
    path('strategies/', strategy_page, name='strategy_page'),
    path("", views.home),
    path("home", views.home, name = 'home'),
    path("backtest", views.backtest, name = 'Backtest'),
    path('mainmenu', views.mainmenu, name='mainmenu'),
    #path('strategy', views.strategy, name='strategy'),
    path('leftmenu', views.leftmenu, name='leftmenu'),
    path('api2', views.api, name='api'),
    path('workingbot', views.workingbot, name='workingbot'),
    path('sift', views.sift, name='sift'),
    path('community', views.community, name='community'),
    path('indicator', views.indicator, name='indicator'),
    path('logout', views.logout, name=''),
    
    
]