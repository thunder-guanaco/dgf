from django.urls import path

from .views import FriendListView, FriendUpdateView, FeedbackCreateView, VideoListView, TournamentListView, \
    bag_tag_claim, bag_tag_new, bag_tag_update, ts_next_tournament, ts_future_dates, FriendDetailView, \
    tournament_attendance, tpl_next_tournament, FriendSearchView, friends_info, all_friend_ids

app_name = 'dgf'
urlpatterns = [

    # PAGES
    path('', FriendListView.as_view(), name='friend_index'),
    path('search/', FriendSearchView.as_view(), name='friend_search'),
    path('profile/', FriendUpdateView.as_view(), name='friend_update'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('media/', VideoListView.as_view(), name='media'),
    path('tournaments/', TournamentListView.as_view(), name='tournament_index'),

    # API
    path('tournaments/<int:tournament_id>/attendance', tournament_attendance, name='tournament_attendance'),
    path('bag-tags/<int:bag_tag>/claim', bag_tag_claim, name='bag_tag_claim'),
    path('bag-tags/new', bag_tag_new, name='bag_tag_new'),
    path('bag-tags/', bag_tag_update, name='bag_tag_update'),
    path('tremonia-series/next-tournament', ts_next_tournament, name='tremonia_series_next_tournament'),
    path('tremonia-putting-liga/next-tournament', tpl_next_tournament, name='tremonia_putting_liga_next_tournament'),

    # API for Disc Golf Metrix JS scripts
    path('disc-golf-metrix/all-friend-ids', all_friend_ids, name='disc_golf_metrix_all_friend_ids'),
    path('disc-golf-metrix/friends', friends_info, name='disc_golf_metrix_friends'),

    # INCLUDES
    # used here: https://discgolfmetrix.com/715021
    path('tremonia-series/future-dates', ts_future_dates, name='tremonia_series_future_dates'),

    # FRIEND PAGE (must be at the end)
    path('<str:slug>/', FriendDetailView.as_view(), name='friend_detail'),
]
