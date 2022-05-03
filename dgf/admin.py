from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import (
    RelatedDropdownFilter
)

from .models import Highlight, DiscInBag, Ace, Feedback, FavoriteCourse, Video, Tournament, Result, Friend, Course, \
    Attendance, Tour, BagTagChange


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
                'bag_tag',
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

    list_display = ('username', 'first_name', 'last_name', 'nickname', 'division', 'bag_tag',
                    'pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    list_editable = ('pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    list_display_links = ('username',)

    list_filter = (
        'is_active',
        ('division', RelatedDropdownFilter),
        ('pdga_number', admin.EmptyFieldListFilter),
        ('gt_number', admin.EmptyFieldListFilter),
        ('udisc_username', admin.EmptyFieldListFilter),
        ('metrix_user_id', admin.EmptyFieldListFilter),
    )

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
        return Result.objects.all().order_by('-division', 'position')


class AttendanceInline(admin.TabularInline):
    model = Attendance

    def get_queryset(self, request):
        return Attendance.objects.all().order_by('friend__first_name')


class TournamentsTourRelationInline(admin.TabularInline):
    model = Tour.tournaments.through

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('tournament__begin')


def recalculate_points(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.recalculate_points()


recalculate_points.short_description = _('Recalculate points')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                ('name', 'active'),
                ('pdga_id', 'gt_id', 'metrix_id'),
                ('begin', 'end'),
                'point_system',
            ]}
         )
    ]

    list_display = ('needs_check', 'name', 'active', 'begin', 'end', 'pdga_id', 'gt_id', 'metrix_id')
    list_editable = ('active', 'pdga_id', 'gt_id', 'metrix_id')
    list_display_links = ('name',)

    search_fields = ('name', 'pdga_id', 'gt_id', 'metrix_id')

    inlines = [
        TournamentsTourRelationInline, ResultInline, AttendanceInline,
    ]

    actions = [recalculate_points]


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'name',
                'division',
                'evaluate_how_many',
                'date',
                'tournament_count',
            ]}
         )
    ]

    readonly_fields = ['date', 'tournament_count']

    list_display = ('name', 'division', 'begin', 'end',)
    search_fields = ('name', 'division')

    inlines = [
        TournamentsTourRelationInline,
    ]
    exclude = ('tournaments',)


@admin.register(BagTagChange)
class BagTagChangeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': [
                'actor',
                ('friend', 'timestamp'),
                ('previous_number', 'new_number'),
            ]}
         )
    ]

    readonly_fields = ['actor', 'friend', 'previous_number', 'new_number', 'timestamp']

    list_display = ('actor', 'friend', 'previous_number', 'new_number', 'timestamp')
    search_fields = ('friend', 'previous_number', 'new_number')
