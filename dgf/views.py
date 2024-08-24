import random
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Func, Value, CharField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from dgf.disc_golf_metrix import disc_golf_metrix, tremonia_series as ts, tremonia_putting_liga as tpl
from dgf.formsets import ace_formset_factory, disc_formset_factory, favorite_course_formset_factory, \
    highlight_formset_factory, video_formset_factory
from dgf.models import Friend, Video, Tournament, Attendance, BagTagChange, GitHubIssue
from dgf_cms.settings import DISC_GOLF_METRIX_TOURNAMENT_PAGE


class FriendListView(ListView):
    template_name = 'dgf/friend_list.html'
    context_object_name = 'friends'
    queryset = Friend.objects.all().order_by('?')


class FriendSearchView(ListView):
    template_name = 'dgf/friend_search.html'
    context_object_name = 'friends'
    queryset = Friend.objects.all().order_by('first_name')


class FriendDetailView(DetailView):
    model = Friend
    slug_field = 'slug'
    template_name = 'dgf/friend_detail.html'
    queryset = (Friend.objects.all().prefetch_related('favorite_courses__course',
                                                      'highlights',
                                                      'discs__disc',
                                                      'aces',
                                                      'videos')
                )


class FriendUpdateView(LoginRequiredMixin, UpdateView):
    model = Friend
    template_name_suffix = '_profile'
    fields = ['main_photo', 'first_name', 'last_name', 'nickname', 'club_role',
              'sponsor', 'sponsor_logo', 'sponsor_link',
              'gt_number', 'udisc_username', 'pdga_number', 'metrix_user_id', 'social_media_agreement',
              'division', 'city', 'plays_since', 'free_text',  # best_score_in_wischlingen TODO: #6282
              'job', 'hobbies']
    formsets = [('favorite_courses', favorite_course_formset_factory),
                ('highlights', highlight_formset_factory),
                ('discs', disc_formset_factory),
                ('aces', ace_formset_factory),
                ('videos', video_formset_factory)]

    def get_object(self, queryset=None):
        return self.request.user.friend

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

    def get_success_url(self):
        return reverse('dgf:friend_detail', args=[self.request.user.friend.slug])


class ExtendedFriendUpdateView(FriendUpdateView):
    template_name_suffix = '_profile_extended'
    fields = []


class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = GitHubIssue
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.friend = self.request.user.friend
        form.type = GitHubIssue.FEEDBACK
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dgf:feedback')


class VideoListView(ListView):
    template_name = 'dgf/media_list.html'
    context_object_name = 'video_urls'

    def get_queryset(self):
        all_videos = list(set(Video.objects.all().values_list('url', flat=True)))
        random.shuffle(all_videos)
        return all_videos


class TournamentListView(LoginRequiredMixin, ListView):
    context_object_name = 'tournaments'
    template_name = 'dgf/tournament_list.html'
    queryset = Tournament.objects.filter(begin__gte=datetime.now()).order_by('begin')


@login_required
@require_http_methods(['POST', 'DELETE'])
def tournament_attendance(request, tournament_id):
    friend = request.user.friend

    if request.method == 'POST':
        _, created = Attendance.objects.get_or_create(friend=friend, tournament_id=tournament_id)
        return HttpResponse(status=201 if created else 204)

    if request.method == 'DELETE':
        Attendance.objects.filter(friend=friend, tournament_id=tournament_id).delete()
        return HttpResponse(status=204)


@login_required
@require_POST
def bag_tag_claim(request, bag_tag):
    taker = request.user.friend

    if not taker.bag_tag:
        return HttpResponse(status=400, reason='Only friends with a bag tag are allowed to claim other.')

    giver = Friend.objects.get(bag_tag=bag_tag)

    taker_bag_tag = taker.bag_tag
    giver_bag_tag = giver.bag_tag

    # take bag tags away
    taker.bag_tag = None
    taker.save()
    giver.bag_tag = None
    giver.save()

    # save new bag tags
    taker.bag_tag = giver_bag_tag
    taker.save()
    giver.bag_tag = taker_bag_tag
    giver.save()

    now = datetime.now()
    BagTagChange.objects.create(actor=request.user.friend,
                                friend=taker,
                                previous_number=taker_bag_tag,
                                new_number=giver_bag_tag,
                                timestamp=now)

    BagTagChange.objects.create(actor=request.user.friend,
                                friend=giver,
                                previous_number=giver_bag_tag,
                                new_number=taker_bag_tag,
                                timestamp=now)

    return HttpResponse(status=204)


def bag_tag_changes_list(friend):
    return list(friend.bag_tag_changes.all()
                .annotate(day=Func(F('timestamp'),
                                   Value('%Y-%m-%d %H:%i:%s'),
                                   function='DATE_FORMAT',
                                   output_field=CharField()))
                .values_list('day', 'new_number')
                )


@require_GET
def bag_tag_history(request):
    return JsonResponse({
        friend.slug: bag_tag_changes_list(friend)
        for friend in Friend.objects.filter(bag_tag__isnull=False)
    })


def get_next_bag_tag():
    return Friend.objects.filter(bag_tag__isnull=False).order_by("-bag_tag")[0].bag_tag + 1


@login_required
@require_POST
def bag_tag_new(request):
    actor = request.user.friend

    if not actor.is_superuser:
        return HttpResponse(status=400, reason='Only admins are allowed to assign new bag tags.')

    friends = sorted(Friend.objects.filter(bag_tag__isnull=True).filter(username__in=request.POST.getlist("players[]")),
                     key=lambda f: f.short_name)

    if friends:
        next_bag_tag = get_next_bag_tag()
        next_bag_tags = list(range(next_bag_tag, next_bag_tag + len(friends)))

        now = datetime.now()

        for friend, bag_tag in zip(friends, next_bag_tags):
            friend.bag_tag = bag_tag
            friend.save()
            BagTagChange.objects.create(actor=actor,
                                        friend=friend,
                                        previous_number=None,
                                        new_number=bag_tag,
                                        timestamp=now)

    return HttpResponse(status=204)


def any_bag_tag_is_given(bag_tags):
    return Friend.objects.filter(bag_tag__in=bag_tags).exists()


@login_required
@require_POST
def bag_tag_update(request):
    actor = request.user.friend

    if not actor.bag_tag:
        return HttpResponse(status=400, reason='Only friends with a bag tag are allowed to change them.')

    current_bag_tags = dict(Friend.objects.filter(username__in=request.POST.keys()).values_list('username', 'bag_tag'))
    new_bag_tags = {key: int(value) for key, value in request.POST.items()}

    if set(current_bag_tags.keys()) != set(new_bag_tags.keys()):
        return HttpResponse(status=400, reason=_('This makes no sense. For these bag tags the users should be: '
                                                 f'{str(sorted(current_bag_tags.keys()))[1:-1]}'))

    if set(current_bag_tags.values()) != set(new_bag_tags.values()):
        bag_tags_diff = set(new_bag_tags.values()) - set(current_bag_tags.values())
        if any_bag_tag_is_given(bag_tags_diff):
            return HttpResponse(status=400, reason=_('This makes no sense. For these users the bag tags should be: '
                                                     f'{str(sorted(current_bag_tags.values()))[1:-1]} '
                                                     'or any other free bag tag'))

    # take bag tags away
    Friend.objects.filter(username__in=request.POST.keys()).update(bag_tag=None)

    now = datetime.now()

    for username, bag_tag in new_bag_tags.items():
        friend = Friend.objects.get(username=username)
        friend.bag_tag = bag_tag
        friend.save()
        BagTagChange.objects.create(actor=actor,
                                    friend=friend,
                                    previous_number=current_bag_tags[username],
                                    new_number=new_bag_tags[username],
                                    timestamp=now,
                                    active=new_bag_tags[username] != current_bag_tags[username])

    return HttpResponse(status=204)


def dgm_next_tournament(query, dgm_root_id):
    next_tournament = disc_golf_metrix.next_tournaments(query).first()
    if next_tournament:
        url = next_tournament.url
    else:
        url = DISC_GOLF_METRIX_TOURNAMENT_PAGE.format(dgm_root_id)

    return redirect(url)


def ts_next_tournament(request):
    return dgm_next_tournament(ts.FILTER, ts.ROOT_ID)


def tpl_next_tournament(request):
    return dgm_next_tournament(tpl.FILTER, tpl.ROOT_ID)


def all_friend_ids(request):
    all_ids = list(Friend.objects.filter(metrix_user_id__isnull=False).values_list('metrix_user_id', flat=True))
    return JsonResponse({'ids': all_ids})


def friends_info(request):
    friends = Friend.objects.filter(metrix_user_id__isnull=False) \
                            .values('metrix_user_id', 'bag_tag')
    return JsonResponse({'friends': list(friends)})


def ts_future_dates(request):
    return render(request, 'dgf/plugins/next_tournaments.html',
                  context={
                      'tournaments': ts.next_tournaments(),
                  })
