from django.urls import path
from . import views

urlpatterns = [

    path("api-connection", views.api_connection, name="api_connection"),


]