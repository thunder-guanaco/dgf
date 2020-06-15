import random

from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from .formsets import FavoriteCourseFormset, HighlightFormset, DiscFormset, AceFormset, VideoFormset
from .models import Friend, Feedback, Video


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