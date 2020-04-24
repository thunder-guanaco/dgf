from django.contrib import admin

from .models import Friend, Highlight, DiscInBag, Course, Ace


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'name',
                ('postal_code', 'city'),
                'country'
            ]}
         )
    ]

    list_display = ('name', 'postal_code', 'city', 'country')

    search_fields = list_display


class HighlightInline(admin.TabularInline):
    model = Highlight


class InTheBagInline(admin.TabularInline):
    model = DiscInBag

    def get_queryset(self, request):
        return DiscInBag.objects.all().order_by('-type')


class AceInline(admin.TabularInline):
    model = Ace


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
                ('plays_since', 'free_text'),
                'favorite_course'
            ]}
         ),
        ('DANGER ZONE!', {
            'fields': [
                'slug'
            ]})
    ]

    inlines = [
        HighlightInline, InTheBagInline, AceInline
    ]

    list_display = ('username', 'first_name', 'last_name', 'pdga_number', 'division')

    search_fields = ('username', 'first_name', 'last_name', 'pdga_number', 'nickname', 'slug')


admin.site.register(Course, CourseAdmin)
admin.site.register(Friend, FriendAdmin)
