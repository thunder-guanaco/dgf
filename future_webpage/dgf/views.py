import random
from datetime import datetime

from django.forms import inlineformset_factory, Select, SelectDateWidget
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from partial_date import PartialDate

from .models import Friend, Highlight, DiscInBag, Ace, Feedback, Video, FavoriteCourse


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


FavoriteCourseFormset = inlineformset_factory(
    Friend, FavoriteCourse, fields=('course',),
    max_num=5, extra=5, validate_max=True
)

HighlightFormset = inlineformset_factory(
    Friend, Highlight, fields=('content',),
    max_num=5, extra=5, validate_max=True
)

DiscFormset = inlineformset_factory(
    Friend, DiscInBag, fields=('type', 'amount', 'disc'), extra=1,
    widgets={'disc': Select(attrs={'class': 'chosen-select'})}
)


class PartialDateWidget(SelectDateWidget):
    is_localized = False

    def format_value(self, value):
        if isinstance(value, PartialDate):
            date = value.date
            return {
                'year': date.year if value.precision >= PartialDate.YEAR else '',
                'month': date.month if value.precision >= PartialDate.MONTH else '',
                'day': date.day if value.precision >= PartialDate.DAY else '',
            }
        else:
            return super().format_value(value)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if not y:
            return None
        date_string = str(y)
        if m:
            date_string += '-{}'.format(m)
        if d:
            date_string += '-{}'.format(d)
        return date_string


current_year = datetime.now().year

AceFormset = inlineformset_factory(
    Friend, Ace, fields=('friend', 'disc', 'course', 'hole', 'type', 'date'),
    extra=0, widgets={'date': PartialDateWidget(years=range(current_year, current_year - 20, -1))}
)

VideoFormset = inlineformset_factory(
    Friend, Video, fields=('url', 'type'),
    extra=0
)


class UpdateView(generic.edit.UpdateView):
    model = Friend
    fields = ['first_name', 'last_name', 'nickname', 'club_role', 'sponsor', 'sponsor_logo', 'sponsor_link',
              'pdga_number', 'division', 'city', 'main_photo', 'plays_since', 'free_text']
    template_name_suffix = '_profile'
    formsets = [('favorite_courses', FavoriteCourseFormset),
                ('highlights', HighlightFormset),
                ('discs', DiscFormset),
                ('aces', AceFormset),
                ('videos', VideoFormset)]

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

        # if any formset is not valid: don't save them
        for formset in self.formsets:
            if not context[formset[0]].is_valid():
                return super().form_invalid(form)

        # save all formsets
        for formset in self.formsets:
            context[formset[0]].instance = self.object
            context[formset[0]].save()

        # save the parent form
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user.friend

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])


class FeedbackCreate(CreateView):
    model = Feedback
    fields = ['title', 'feedback']

    def form_valid(self, form):
        form.instance.friend = self.request.user.friend
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])


class MediaIndex(generic.ListView):
    template_name = 'dgf/media_list.html'
    context_object_name = 'video_urls'

    def get_queryset(self):
        all_videos = list(set(Video.objects.all().values_list('url', flat=True)))
        random.shuffle(all_videos)
        return all_videos
