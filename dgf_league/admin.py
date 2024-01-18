from datetime import datetime

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from .models import Team, TeamMembership, Match, Result, POINTS_PER_MATCH, FriendWithoutTeam, first_league_year


class YearFilter(admin.SimpleListFilter):
    title = _('Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        current_year = datetime.today().year
        return [(year, str(year)) for year in range(first_league_year(), current_year + 1)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                created__year=self.value(),
            )
        else:
            return queryset


class AdminWithActor(admin.ModelAdmin):

    def get_changeform_initial_data(self, request):
        data = super(AdminWithActor, self).get_changeform_initial_data(request)
        data['actor'] = str(request.user.friend.id)
        return data


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 0
    min_num = 2
    max_num = 2
    can_delete = False


@admin.register(Team)
class TeamAdmin(AdminWithActor):
    fieldsets = (
        ('', {
            'fields': (
                'year',
                'name',
                'actor',
                'created'
            )}
         ),
    )

    list_display = ('year', 'name', 'member_names', 'actor', 'created')
    list_display_links = ('name',)
    list_filter = [YearFilter]
    readonly_fields = ('year', 'created')
    search_fields = ('name', 'year')
    inlines = (TeamMembershipInline,)


class ResultInlineFormSet(BaseInlineFormSet):

    def check_teams(self):
        teams = [form.cleaned_data["team"] for form in self.forms]
        if teams[0] == teams[1]:
            raise ValidationError(_('Please select 2 different teams'))
        if Match.objects.filter(results__team=teams[0]).filter(results__team=teams[1]):
            raise ValidationError(_('That result already exist. '
                                    'Please select it from the list and change it instead of creating a new one'))

    def check_total_points(self):
        total_points = sum(form.cleaned_data['points'] for form in self.forms)
        if total_points != POINTS_PER_MATCH:
            raise ValidationError(_('Sum of all points should be %(points)s') % {'points': POINTS_PER_MATCH})

    def clean(self):

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        self.check_teams()
        self.check_total_points()


class ResultInline(admin.TabularInline):
    model = Result
    formset = ResultInlineFormSet
    extra = 0
    min_num = 2
    max_num = 2
    can_delete = False


@admin.register(Match)
class MatchAdmin(AdminWithActor):
    fieldsets = (
        ('', {
            'fields': (
                'year',
                'actor',
                'created'
            )}
         ),
    )

    list_display = ('year', 'results_as_str', 'actor', 'created')
    list_display_links = ('results_as_str',)
    list_filter = [YearFilter]
    readonly_fields = ('year', 'created')
    search_fields = ('results__team__name', 'year')
    inlines = (ResultInline,)


@admin.register(FriendWithoutTeam)
class FriendWithoutTeamAdmin(admin.ModelAdmin):
    list_display = ('friend',)
    search_fields = ('friend__nickname', 'friend__first_name', 'friend__last_name')
