import re

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import admin as auth_admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

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
    BASIC_FIELDS = (
        ('username', 'slug'),
        ('first_name', 'last_name'),
        ('nickname',),
        ('is_active',),
        ('social_media_agreement',),
    )
    EXTERNAL_IDS_FIELDS = (
        ('pdga_number', 'gt_number'),
        ('udisc_username', 'metrix_user_id')
    )

    add_fieldsets = (
        ('Basic', {
            'fields': BASIC_FIELDS + ('password1', 'password2')
        }),
        ('External IDs', {
            'fields': EXTERNAL_IDS_FIELDS
        })
    )

    fieldsets = (
        ('Basic', {
            'fields': BASIC_FIELDS + ('password',)
        }),
        ('External IDs', {
            'fields': EXTERNAL_IDS_FIELDS
        }),
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
                'plays_since',
                'best_score_in_wischlingen',
                'free_text',
                'job',
                'hobbies'
            )}
         ),
    )

    ordering = ('-is_active', 'first_name',)

    list_display = ('is_active', 'username', 'first_name', 'last_name', 'nickname', 'bag_tag',
                    'pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    list_editable = ('pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    list_display_links = ('username',)

    list_filter = (
        'is_active',
        ('pdga_number', admin.EmptyFieldListFilter),
        ('gt_number', admin.EmptyFieldListFilter),
        ('udisc_username', admin.EmptyFieldListFilter),
        ('metrix_user_id', admin.EmptyFieldListFilter)
    )

    search_fields = ('username', 'first_name', 'last_name', 'nickname', 'slug',
                     'pdga_number', 'gt_number', 'udisc_username', 'metrix_user_id')

    inlines = (FavoriteCourseInline, HighlightInline, InTheBagInline, AceInline, VideoInline)

    def get_inlines(self, request, obj):
        if not obj:
            return ()
        return self.inlines

    def response_post_save_change(self, request, obj):
        profile_url = reverse('dgf:friend_detail', args=[obj.slug])

        if '_save' in request.POST:
            message = mark_safe(f'{_("See profile")}: <a href="{profile_url}">{obj}</a>')
            self.message_user(request, message, level=messages.INFO)
            return super(FriendAdmin, self).response_post_save_change(request, obj)

        if '_save_and_to_to_profile' in request.POST:
            return HttpResponseRedirect(profile_url)

        else:
            return super(FriendAdmin, self).response_post_save_change(request, obj)


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


def is_current_tournament_tremonia_series(request):
    search = re.search(r'/admin/dgf/tournament/(?P<id>\d+)/change/', request.get_full_path())
    tournament_id = search.group('id')
    tournament = Tournament.objects.get(id=tournament_id)
    return tournament.name.startswith('Tremonia Series #')


class OnlyFriendsInFieldsInline(admin.TabularInline):

    def get_field_queryset(self, db, db_field, request):
        field_queryset = super().get_field_queryset(db, db_field, request)

        if db_field.name == 'friend':
            if is_current_tournament_tremonia_series(request):
                field_queryset = field_queryset.order_by('first_name')
            else:
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
                'name',
                'active',
                'pdga_id',
                'gt_id',
                'metrix_id',
                'begin',
                'end',
                'point_system'
            )}
         ),
    )

    list_display = ('needs_check', 'name', 'active', 'begin', 'end', 'pdga_id', 'gt_id', 'metrix_id')
    list_editable = ('active', 'pdga_id', 'gt_id', 'metrix_id')
    list_display_links = ('name',)

    search_fields = ('name', 'pdga_id', 'gt_id', 'metrix_id')

    inlines = (TournamentsTourRelationInline, ResultInline, AttendanceInline)

    def get_inlines(self, request, obj):
        return self.inlines if obj else []

    actions = (recalculate_points, reimport_attendance, reimport_results)

    def needs_check(self, obj):
        if obj.first_positions_are_ok:
            color = 'green'
            label = _('OK')
        else:
            color = 'red'
            label = _('please check')
        return format_html(
            '<span style="color: {};">{}</span>',
            color, label,
        )


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
                'friend',
                'timestamp',
                'previous_number',
                'new_number',
                'active'
            )}
         ),
    )

    ordering = ('-timestamp', 'new_number')

    readonly_fields = ('actor', 'friend', 'previous_number', 'new_number', 'timestamp', 'active')

    list_display = ('actor', 'friend', 'previous_number', 'new_number', 'timestamp', 'active')
    search_fields = ('friend', 'previous_number', 'new_number')
