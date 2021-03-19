from django.contrib import admin

from .models import Ativo, HistoricalData

admin.site.register(Ativo)
admin.site.register(HistoricalData)
