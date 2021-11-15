from django.contrib import admin

from .models import Highlight, DiscInBag, Ace, Feedback, FavoriteCourse, Video, Tournament, Result, Friend, Course, \
    Attendance, Tour


@admin.register(Course)
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


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic', {
            'fields': [
                ('username', 'slug'),
                ('first_name', 'last_name', 'nickname'),
            ]}
         ),
        ('External IDs', {
            'fields': [
                ('pdga_number', 'gt_number'),
                ('udisc_username', 'metrix_user_id'),
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
    ]

    inlines = [
        FavoriteCourseInline, HighlightInline, InTheBagInline, AceInline, VideoInline
    ]

    list_display = ('username', 'first_name', 'last_name', 'nickname', 'pdga_number', 'division')
    search_fields = ('username', 'first_name', 'last_name', 'nickname', 'slug', 'udisc_username', 'pdga_number')


@admin.register(Feedback)
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


class ResultInline(admin.TabularInline):
    model = Result

    def get_queryset(self, request):
        return Result.objects.all().order_by('position')


class AttendanceInline(admin.TabularInline):
    model = Attendance

    def get_queryset(self, request):
        return Attendance.objects.all().order_by('friend__first_name')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'name',
                ('pdga_id', 'gt_id', 'metrix_id'),
                ('begin', 'end'),
                'url',
                'tour',
                'point_system',
            ]}
         )
    ]

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "point_system":
            kwargs['choices'] = (
                ('accepted', 'Accepted'),
                ('denied', 'Denied'),
            )
            if request.user.is_superuser:
                kwargs['choices'] += (('ready', 'Ready for deployment'),)
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    list_display = ('needs_check', 'name', 'begin', 'end', 'pdga_id', 'gt_id', 'metrix_id', 'tour')
    list_display_links = ('name',)
    search_fields = ('name', 'pdga_id', 'gt_id', 'metrix_id')

    inlines = [
        ResultInline, AttendanceInline
    ]


class TournamentInline(admin.TabularInline):
    model = Tournament
    extra = 0

    def get_queryset(self, request):
        return Tournament.objects.all().order_by('begin', 'end')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'name',
            ]}
         )
    ]

    list_display = ('name', 'begin', 'end')
    search_fields = ('name',)

    inlines = [
        TournamentInline
    ]
