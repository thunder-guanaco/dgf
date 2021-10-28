import datetime
import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from dgf.formsets import ace_formset_factory, disc_formset_factory, favorite_course_formset_factory, \
    highlight_formset_factory, video_formset_factory
from dgf.models import Friend, Feedback, Video, Tournament, Attendance


class IndexView(generic.ListView):
    template_name = 'dgf/friend_list.html'
    context_object_name = 'friends'
    queryset = Friend.objects.all().order_by('?')


class DetailView(generic.DetailView):
    model = Friend
    slug_field = 'slug'
    template_name = 'dgf/friend_detail.html'
    queryset = (Friend.objects.all().prefetch_related('favorite_courses__course',
                                                      'highlights',
                                                      'discs__disc',
                                                      'aces',
                                                      'videos')
                )


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Friend
    fields = ['first_name', 'last_name', 'nickname', 'club_role', 'sponsor', 'sponsor_logo', 'sponsor_link',
              'pdga_number', 'division', 'city', 'main_photo', 'plays_since', 'best_score_in_wischlingen', 'free_text',
              'job', 'hobbies']
    template_name_suffix = '_profile'
    formsets = [('favorite_courses', favorite_course_formset_factory),
                ('highlights', highlight_formset_factory),
                ('discs', disc_formset_factory),
                ('aces', ace_formset_factory),
                ('videos', video_formset_factory)]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        for formset_name, formset_factory in self.formsets:
            if self.request.POST:
                data[formset_name] = formset_factory()(self.request.POST, instance=self.object)
            else:
                data[formset_name] = formset_factory()(instance=self.object)

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


class FeedbackCreate(LoginRequiredMixin, CreateView):
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


class TournamentsView(generic.ListView):
    context_object_name = 'tournaments'
    template_name = 'dgf/tournament_list.html'
    queryset = Tournament.objects.filter(begin__gte=datetime.datetime.now()).order_by('begin')


@login_required
def attendance(request, tournament_id):
    friend = request.user.friend

    if request.method == 'POST':
        attendance, created = Attendance.objects.get_or_create(friend=friend, tournament_id=tournament_id)
        return HttpResponse(status=201 if created else 204)

    if request.method == 'DELETE':
        Attendance.objects.filter(friend=friend, tournament_id=tournament_id).delete()
        return HttpResponse(status=204)

    return HttpResponse(status=405, reason='Only POST or DELETE methods are allowed here.')


class TremoniaSeriesHallOfFame(generic.ListView):
    context_object_name = 'friends'
    template_name = 'dgf/tremonia_series_hall_of_fame.html'
    queryset = Friend.objects.filter(tremonia_series_wins__gt=0).order_by('-tremonia_series_wins')
