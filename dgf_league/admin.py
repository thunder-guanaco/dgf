from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from .models import Team, TeamMembership, Match, Result, POINTS_PER_MATCH


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
                'name',
                'actor',
            )}
         ),
    )

    list_display = ('name', 'member_names', 'created', 'actor')
    search_fields = ('name',)
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
            raise ValidationError(_(f'Sum of all points should be %(points)s') % {'points': POINTS_PER_MATCH})

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
                'actor',
            )}
         ),
    )

    list_display = ('results_as_str', 'date', 'actor')
    list_display_links = ('results_as_str',)
    search_fields = ('results__team__name',)
    inlines = (ResultInline,)
