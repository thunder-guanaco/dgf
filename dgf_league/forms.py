from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from dgf.models import Friend
from dgf_league.models import POINTS_PER_MATCH, Team
from dgf_league.templatetags.dgf_league import current_year_membership_exists


def format_errors(errors):
    return ', '.join(', '.join(error.messages) for error in errors)


class DgfLeagueAddForm(forms.Form):
    def format_label(self, field):
        if field == '__all__':
            return _('Error')
        return self.fields[field].label

    def errors_as_str(self):
        return '\n'.join(f'{self.format_label(field)}: {format_errors(errors)}'
                         for field, errors in self.errors.as_data().items())


class AddTeamForm(DgfLeagueAddForm):
    actor = forms.ModelChoiceField(label=_('Actor'), queryset=Friend.objects.all())
    partner = forms.ModelChoiceField(label=_('Partner'), queryset=Friend.objects.all())
    name = forms.CharField(label=_('Name'), max_length=100)

    def clean_actor(self):
        actor = self.cleaned_data['actor']
        if current_year_membership_exists(actor):
            raise ValidationError(_('You are already in another team'))
        return actor

    def clean_partner(self):
        partner = self.cleaned_data['partner']
        if current_year_membership_exists(partner):
            raise ValidationError(_('The selected partner is already in another team'))
        return partner

    def clean_name(self):
        name = self.cleaned_data['name']
        if Team.objects.filter(name=name).exists():
            raise ValidationError(_('That name is already taken'))
        return name

    def clean(self):
        if any(self.errors):
            # Don't bother validating anything else until each field is valid on its own
            return

        if self.cleaned_data['actor'] == self.cleaned_data['partner']:
            raise ValidationError(_('You can not select yourself as partner'))


class AddResultForm(DgfLeagueAddForm):
    own_team = forms.ModelChoiceField(label=_('Own team'), queryset=Team.objects.all())
    rival_team = forms.ModelChoiceField(label=_('Rival team'), queryset=Team.objects.all())
    own_points = forms.IntegerField(label=_('Own points'), min_value=0, max_value=POINTS_PER_MATCH)
    rival_points = forms.IntegerField(label=_('Rival points'), min_value=0, max_value=POINTS_PER_MATCH)

    def clean(self):
        if any(self.errors):
            # Don't bother validating anything else until each field is valid on its own
            return

        if self.cleaned_data['own_team'] == self.cleaned_data['rival_team']:
            raise ValidationError(_('Please select 2 different teams'))

        if (self.cleaned_data['own_points'] + self.cleaned_data['rival_points']) != POINTS_PER_MATCH:
            raise ValidationError(_('Sum of all points should be %(points)s') % {'points': POINTS_PER_MATCH})
