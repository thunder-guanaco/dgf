from django.contrib import admin

from .models import Friend, Highlight


class HighlightInline(admin.TabularInline):
    model = Highlight


class FriendAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'username',
                ('first_name', 'last_name', 'nickname'),
                'pdga_number',
                'division',
                'city',
                'main_photo',
                ('plays_since', 'free_text')
            ]}
         ),
        ('DANGER ZONE!', {
            'fields': [
                'slug'
            ]})
    ]

    inlines = [
        HighlightInline,
    ]

    list_display = ('username', 'first_name', 'last_name', 'pdga_number', 'division')

    search_fields = ('username', 'first_name', 'last_name', 'pdga_number', 'nickname', 'slug')


admin.site.register(Friend, FriendAdmin)
