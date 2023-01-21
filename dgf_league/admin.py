from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Team, TeamMembership, Result


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 0
    min_num = 2
    max_num = 2
    can_delete = False


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {
            'fields': (
                'name',
            )}
         ),
    )

    list_display = ('name', 'get_members', 'created')
    search_fields = ('name',)
    inlines = (TeamMembershipInline,)

    @admin.display(ordering='team__members', description=_('Members'))
    def get_members(self, obj):
        return [membership.friend for membership in obj.members.all()]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {
            'fields': (
                ('team1', 'points1'),
                ('team2', 'points2')
            )}
         ),
    )

    list_display = ('team1', 'points1', 'points2', 'team2')
    search_fields = ('team1', 'team2')
    list_display_links = search_fields
