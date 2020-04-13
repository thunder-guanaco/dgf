from django.forms import inlineformset_factory
from django.urls import reverse
from django.views import generic

from .models import Friend, Highlight


class IndexView(generic.ListView):
    template_name = 'dgf/friend_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return Friend.objects.all()


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


class UpdateView(generic.edit.UpdateView):
    model = Friend
    fields = ['first_name', 'last_name', 'nickname', 'pdga_number', 'city', 'main_photo',
              'plays_since', 'free_text']
    template_name_suffix = '_profile'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["highlights"] = HighlightFormset(self.request.POST, instance=self.object)
        else:
            data["highlights"] = HighlightFormset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        children = context["highlights"]
        self.object = form.save()
        if children.is_valid():
            children.instance = self.object
            children.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.friend

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])
