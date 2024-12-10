from django.contrib import admin
from .models import Api

class ApiAdmin(admin.ModelAdmin):
    list_display = ("name","secretkey","adress")
    search_fields = ("name",)
    #readonly_fields = ("api_adress","api_secretkey",)

# Register your models here.
admin.site.register(Api, ApiAdmin)

