from django.urls import path
from . import views

urlpatterns = [

    path("api-connection", views.api_connection, name="api_connection"),
    path('api/api/', views.list_api, name='list_apis'),
    path('api/apis/', views.add_api, name='add_api'),
    path('api-connection/api/', views.get_api, name='get_api'),

]