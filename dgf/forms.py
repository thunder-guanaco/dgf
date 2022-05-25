from django import forms

from djangocms_picture.forms import PictureForm

from dgf.models import DiscGolfMetrixResultPluginModel


class TournamentResultForm(PictureForm):

    class Meta:
        model = DiscGolfMetrixResultPluginModel
        fields = '__all__'
        widgets = {
            'metrix_url': forms.TextInput(),
        }
