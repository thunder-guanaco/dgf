from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

from .models import Team, TeamMembership, Match, Result, MAX_POINTS_PER_MATCH


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

    list_display = ('name', 'member_names', 'created')
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
        if total_points != MAX_POINTS_PER_MATCH:
            raise ValidationError(_(f'Sum of all points should be {MAX_POINTS_PER_MATCH}'))

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
class MatchAdmin(admin.ModelAdmin):
    list_display = ('results_as_str', 'date')
    list_display_links = ('results_as_str',)
    search_fields = ('results_as_str',)
    inlines = (ResultInline,)
