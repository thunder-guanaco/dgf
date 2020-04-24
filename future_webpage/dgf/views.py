from django.forms import inlineformset_factory, Select
from django.urls import reverse
from django.views import generic

from .models import Friend, Highlight, DiscInBag


class IndexView(generic.ListView):
    template_name = 'dgf/friend_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return Friend.objects.all().order_by('?')


class DetailView(generic.DetailView):
    model = Friend
    slug_field = 'slug'
    template_name = 'dgf/friend_detail.html'

    def get_queryset(self):
        return Friend.objects.all()


HighlightFormset = inlineformset_factory(
    Friend, Highlight, fields=('content',),
    max_num=5, extra=5, validate_max=True
)

DiscFormset = inlineformset_factory(
    Friend, DiscInBag, fields=('type', 'amount', 'disc'), extra=1,
    widgets={'disc': Select(attrs={'class': 'chosen-select'})}
)


class UpdateView(generic.edit.UpdateView):
    model = Friend
    fields = ['first_name', 'last_name', 'nickname', 'sponsor', 'sponsor_logo', 'pdga_number', 'division',
              'city', 'main_photo', 'plays_since', 'free_text', 'favorite_course']
    template_name_suffix = '_profile'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['highlights'] = HighlightFormset(self.request.POST, instance=self.object)
            data['discs'] = DiscFormset(self.request.POST, instance=self.object)
        else:
            data['highlights'] = HighlightFormset(instance=self.object)
            data['discs'] = DiscFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save()

        if context['highlights'].is_valid():
            context['highlights'].instance = self.object
            context['highlights'].save()
        else:
            return super().form_invalid(form)

        if context['discs'].is_valid():
            context['discs'].instance = self.object
            context['discs'].save()
        else:
            return super().form_invalid(form)

        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.friend

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])
