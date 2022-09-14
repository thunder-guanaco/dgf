from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import (
    RelatedDropdownFilter
)

from . import german_tour
from .models import Highlight, DiscInBag, Ace, GitHubIssue, FavoriteCourse, Video, Tournament, Result, Friend, Course, \
    Attendance, Tour, BagTagChange


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    fieldsets = (
        ('', {
            'fields': (
                'name',
                ('postal_code', 'city'),
                'country'
            )}
         ),
        ('UDisc', {
            'fields': (
                'udisc_id',
                'udisc_main_layout'
            )}
         )
    )

    list_display = ('name', 'postal_code', 'city', 'country', 'udisc_id')
    search_fields = list_display


class FavoriteCourseInline(admin.TabularInline):
    model = FavoriteCourse


class HighlightInline(admin.TabularInline):
    model = Highlight


class InTheBagInline(admin.TabularInline):
    model = DiscInBag
    ordering = ('-type',)


class AceInline(admin.TabularInline):
    model = Ace
    ordering = ('date',)


class VideoInline(admin.TabularInline):
    model = Video


@admin.register(Friend)
class FriendAdmin(auth_admin.UserAdmin):

    add_fieldsets = (
        ('Basic', {
            'fields': (
                ('username', 'slug'),
                ('first_name', 'last_name', 'nickname'),
                ('is_active',),
                ('password1', 'password2')
            )}
         ),
        ('External IDs', {
            'fields': (
                ('pdga_number', 'gt_number'),
                ('udisc_username', 'metrix_user_id')
            )}
         )
    )

    fieldsets = (
        ('Basic', {
            'fields': (
                ('username', 'slug'),
                ('first_name', 'last_name', 'nickname'),
                ('is_active', 'password')
            )}
         ),
        ('External IDs', {
            'fields': (
                ('pdga_number', 'gt_number'),
                ('udisc_username', 'metrix_user_id')
            )}
         ),
        ('Rest', {
            'fields': (
                'bag_tag',
                'club_role',
                'sponsor',
                'sponsor_logo',
                'sponsor_link',
                'division',
                'city',
                'main_photo',
                ('plays_since', 'best_score_in_wischlingen', 'free_text'),
                ('job', 'hobbies')
            )}
         )
    )

    ordering = ('first_name',)

    list_display = ('is_active', 'username', 'first_name', 'last_name', 'nickname', 'division', 'bag_tag',
                    'pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    list_editable = ('pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    list_display_links = ('username',)

    list_filter = (
        'is_active',
        ('division', RelatedDropdownFilter),
        ('pdga_number', admin.EmptyFieldListFilter),
        ('gt_number', admin.EmptyFieldListFilter),
        ('udisc_username', admin.EmptyFieldListFilter),
        ('metrix_user_id', admin.EmptyFieldListFilter)
    )

    search_fields = ('username', 'first_name', 'last_name', 'nickname', 'slug', 'udisc_username', 'pdga_number')

    inlines = (FavoriteCourseInline, HighlightInline, InTheBagInline, AceInline, VideoInline)

    def get_inlines(self, request, obj):
        if not obj:
            return ()
        return self.inlines


@admin.register(GitHubIssue)
class GitHubIssueAdmin(admin.ModelAdmin):

    fieldsets = (
        ('', {
            'fields': (
                'type',
                'title',
                'body',
                'friend'
            )}
         ),
    )

    list_display = ('type', 'title', 'body', 'friend')
    list_display_links = ('title',)
    search_fields = list_display


class OnlyFriendsInFieldsInline(admin.TabularInline):

    def get_field_queryset(self, db, db_field, request):
        field_queryset = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'friend':
            field_queryset = field_queryset.filter(is_active=True)
        return field_queryset


class ResultInline(OnlyFriendsInFieldsInline):
    model = Result
    ordering = ('-division', 'position')


class AttendanceInline(OnlyFriendsInFieldsInline):
    model = Attendance
    ordering = ('friend__first_name',)


class TournamentsTourRelationInline(admin.TabularInline):
    model = Tour.tournaments.through
    ordering = ('-tour__division', 'tour__name')


def recalculate_points(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.recalculate_points()


recalculate_points.short_description = _('Recalculate points')


def reimport_attendance(modeladmin, request, queryset):
    for tournament in queryset.filter(gt_id__isnull=False):
        german_tour.update_tournament_attendance(tournament)


reimport_attendance.short_description = _('Reimport attendance from turniere.discgolf.de')


def reimport_results(modeladmin, request, queryset):
    for tournament in queryset.filter(gt_id__isnull=False):
        german_tour.update_tournament_results(tournament)


reimport_results.short_description = _('Reimport results from turniere.discgolf.de')


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):

    fieldsets = (
        ('', {
            'fields': (
                ('name', 'active'),
                ('pdga_id', 'gt_id', 'metrix_id'),
                ('begin', 'end'),
                'point_system'
            )}
         ),
    )

    list_display = ('needs_check', 'name', 'active', 'begin', 'end', 'pdga_id', 'gt_id', 'metrix_id')
    list_editable = ('active', 'pdga_id', 'gt_id', 'metrix_id')
    list_display_links = ('name',)

    search_fields = ('name', 'pdga_id', 'gt_id', 'metrix_id')

    inlines = (TournamentsTourRelationInline, ResultInline, AttendanceInline)

    actions = (recalculate_points, reimport_attendance, reimport_results)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):

    fieldsets = (
        ('', {
            'fields': (
                'name',
                'division',
                'evaluate_how_many',
                'date',
                'tournament_count'
            )}
         ),
    )

    ordering = ('-division', 'name')

    readonly_fields = ('date', 'tournament_count')

    list_display = ('name', 'division', 'begin', 'end')
    search_fields = ('name', 'division')

    inlines = (TournamentsTourRelationInline,)
    exclude = ('tournaments',)


@admin.register(BagTagChange)
class BagTagChangeAdmin(admin.ModelAdmin):

    fieldsets = (
        ('', {
            'fields': (
                'actor',
                ('friend', 'timestamp'),
                ('previous_number', 'new_number'),
                'active'
            )}
         ),
    )

    ordering = ('-timestamp', 'new_number')

    readonly_fields = ('actor', 'friend', 'previous_number', 'new_number', 'timestamp', 'active')

    list_display = ('actor', 'friend', 'previous_number', 'new_number', 'timestamp', 'active')
    search_fields = ('friend', 'previous_number', 'new_number')
