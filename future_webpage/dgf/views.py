from datetime import datetime

from django.forms import inlineformset_factory, Select, SelectDateWidget
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from .models import Friend, Highlight, DiscInBag, Ace, Feedback


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

AceFormset = inlineformset_factory(
    Friend, Ace, fields=('friend', 'disc', 'course', 'hole', 'type', 'date'),
    extra=0, widgets={'date': SelectDateWidget(years=range(2000, datetime.now().year + 1))}
)


class FeedbackCreate(CreateView):
    model = Feedback
    fields = ['title', 'feedback']

    def form_valid(self, form):
        form.instance.friend = self.request.user.friend
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])


class UpdateView(generic.edit.UpdateView):
    model = Friend
    fields = ['first_name', 'last_name', 'nickname', 'club_role', 'sponsor', 'sponsor_logo', 'sponsor_link',
              'pdga_number', 'division', 'city', 'main_photo', 'plays_since', 'free_text', 'favorite_course']
    template_name_suffix = '_profile'
    formsets = [('highlights', HighlightFormset),
                ('discs', DiscFormset),
                ('aces', AceFormset)]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        for formset in self.formsets:
            if self.request.POST:
                data[formset[0]] = formset[1](self.request.POST, instance=self.object)
            else:
                data[formset[0]] = formset[1](instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save()

        for formset in self.formsets:
            if context[formset[0]].is_valid():
                context[formset[0]].instance = self.object
                context[formset[0]].save()
            else:
                return super().form_invalid(form)

        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.friend

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])
