from django.contrib import admin
from django.utils.html import format_html


from .models import Friend

class FriendAdmin(admin.ModelAdmin):

    fieldsets = [
            ('', {'fields': [('first_name', 'last_name'), 'pdga_number', 'city', 'main_photo']}),
    ]
    
    list_display = ('username', 'first_name', 'last_name', 'pdga_number')
    search_fields = ('username', 'first_name', 'last_name', 'pdga_number')

admin.site.register(Friend, FriendAdmin)
