from django.contrib import admin
from .models import Indicator, Coins

class IndicatorAdmin(admin.ModelAdmin):
    list_display = ("title","on_graph",)
    #list_editable = ("on_graph",)
    search_fields = ("code",)
    readonly_fields = ("code",)

class CoinsAdmin(admin.ModelAdmin):
    list_display = ("name","symbol",)
    search_fields = ('name', 'symbol')

# Register your models here.
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(Coins, CoinsAdmin)
