from django.shortcuts import render
from django.views.generic import TemplateView

from dgf.disc_golf_metrix import tremonia_series as ts
from dgf.views import dgm_next_tournament


# PAGES


class HomeView(TemplateView):
    extra_context = {
        'tournaments': ts.next_tournaments(),
    }

    template_name = 'dgf_tremonia_series/index.html'


# INCLUDES


def next_tournaments_include(request):
    return render(request, 'includes/next_tournaments.html',
                  context={
                      'tournaments': ts.next_tournaments(),
                  })


# REDIRECTS


def next_tournament_redirect(request):
    return dgm_next_tournament(ts.FILTER, ts.ROOT_ID)
