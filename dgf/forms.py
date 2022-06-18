from django import forms

from djangocms_picture.forms import PictureForm

from dgf.models import TournamentResultsPluginModel


class TournamentResultForm(PictureForm):

    class Meta:
        model = TournamentResultsPluginModel
        fields = '__all__'
        widgets = {
            'metrix_url': forms.TextInput(),
        }
