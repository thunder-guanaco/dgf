from django.contrib import admin

from .models import MetrixIds


@admin.register(MetrixIds)
class MetrixIdsAdmin(admin.ModelAdmin):
    list_display = ('ids',)
