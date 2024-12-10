from django.urls import path
from . import views

urlpatterns = [
    # İNDİCATOR URLS
    path('indicators/', views.indicators_page, name='indicators_page'),
    path('api/indicator/', views.list_indicators, name='list_indicators'),
    path('api/indicators/', views.add_indicator, name='add_indicator'),
    path('api/indicator/<int:id>/', views.update_indicator, name='update_indicator'),
    path('api/indicators/<int:id>/', views.get_indicator, name='get_indicator'),
    path('api/indicatordel/<int:id>/', views.del_indicator, name='del_indicator'),

    # GRAPH URLS
    path('api/graph/', views.main_graph, name='main_graph'),
    path('api/graph/<int:id>/', views.update_graph, name='update_graph'),
]
