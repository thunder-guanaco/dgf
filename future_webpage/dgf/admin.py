from django.contrib import admin

from .models import Friend


class FriendAdmin(admin.ModelAdmin):

    fieldsets = [
            ('', {'fields': ['username', ('first_name', 'last_name', 'nickname'), 'pdga_number', 'city', 'main_photo']}),
            ('DANGER ZONE!', {'fields': ['slug']})
    ]
    
    list_display = ('username', 'first_name', 'last_name', 'pdga_number')
    search_fields = ('username', 'first_name', 'last_name', 'pdga_number', 'nickname', 'slug')


admin.site.register(Friend, FriendAdmin)
