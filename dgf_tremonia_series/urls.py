from django.urls import path

from .views import HomeView, next_tournaments_include, next_tournament_redirect

app_name = 'dgf'
urlpatterns = [

    # PAGES
    path('', HomeView.as_view(), name='index'),

    # INCLUDES
    # will be used here: https://discgolfmetrix.com/715021
    path('includes/next-tournaments', next_tournaments_include, name='next-tournaments-include'),

    # REDIRECTS
    # will be used here: https://discgolffriends.de/ts
    path('redirects/next-tournament', next_tournament_redirect, name='next-tournaments-redirect'),
]
