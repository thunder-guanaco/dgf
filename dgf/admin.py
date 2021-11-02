from django.contrib import admin

from .models import Friend, Highlight, DiscInBag, Course, Ace, Feedback, FavoriteCourse, Video, Tournament


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'name',
                ('postal_code', 'city'),
                'country'
            ]}
         ),
        ('UDisc', {
            'fields': [
                'udisc_id',
                'udisc_main_layout'
            ]}
         )
    ]

    list_display = ('name', 'postal_code', 'city', 'country', 'udisc_id')
    search_fields = list_display


class FavoriteCourseInline(admin.TabularInline):
    model = FavoriteCourse


class HighlightInline(admin.TabularInline):
    model = Highlight


class InTheBagInline(admin.TabularInline):
    model = DiscInBag

    def get_queryset(self, request):
        return DiscInBag.objects.all().order_by('-type')


class AceInline(admin.TabularInline):
    model = Ace


class VideoInline(admin.TabularInline):
    model = Video


class FriendAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic', {
            'fields': [
                'username',
                ('first_name', 'last_name', 'nickname'),
            ]}
         ),
        ('External IDs', {
            'fields': [
                'pdga_number',
                'gt_number',
                'udisc_username',
                'metrix_user_id',
            ]}
         ),
        ('Rest', {
            'fields': [
                'club_role',
                'sponsor',
                'sponsor_logo',
                'sponsor_link',
                'division',
                'city',
                'main_photo',
                ('plays_since', 'best_score_in_wischlingen', 'free_text'),
                ('job', 'hobbies'),
            ]}
         ),
        ('DANGER ZONE!', {
            'fields': [
                'slug'
            ]}
         )
    ]

    inlines = [
        FavoriteCourseInline, HighlightInline, InTheBagInline, AceInline, VideoInline
    ]

    list_display = ('username', 'first_name', 'last_name', 'nickname', 'pdga_number', 'division')
    search_fields = ('username', 'first_name', 'last_name', 'nickname', 'slug', 'udisc_username', 'pdga_number')


class FeedbackAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'title',
                'feedback',
                'friend'
            ]}
         )
    ]

    list_display = ('title', 'feedback', 'friend')
    search_fields = list_display


class TournamentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'name',
                ('begin', 'end')
            ]}
         )
    ]

    list_display = ('name', 'begin', 'end')
    search_fields = ('name',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Tournament, TournamentAdmin)
