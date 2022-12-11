from django.http import Http404
from django.shortcuts import render

IMAGE_GENERATORS = [
    'text-with-friends-background',
    'tournament-results',
    'tour-results',
    'picture-with-title',
    'ratings-update',
]


def index(request):
    return render(request, 'dgf_images/generators/index.html', {'image_generators': IMAGE_GENERATORS})


def generator(request, slug):
    if slug in IMAGE_GENERATORS:
        return render(request, f'dgf_images/generators/{slug}.html', {'image_generator': slug})
    else:
        raise Http404(f'There\'s no generator with the given slug: {slug}')
