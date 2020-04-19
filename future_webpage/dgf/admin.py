from django.contrib import admin

from .models import Friend, Highlight, DiscInBag


class HighlightInline(admin.TabularInline):
    model = Highlight


class InTheBagInline(admin.TabularInline):
    model = DiscInBag

    def get_queryset(self, request):
        return DiscInBag.objects.all().order_by('-type')


class FriendAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'username',
                ('first_name', 'last_name', 'nickname'),
                'sponsor',
                'sponsor_logo',
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
        HighlightInline, InTheBagInline
    ]

    list_display = ('username', 'first_name', 'last_name', 'pdga_number', 'division')

    search_fields = ('username', 'first_name', 'last_name', 'pdga_number', 'nickname', 'slug')


admin.site.register(Friend, FriendAdmin)
