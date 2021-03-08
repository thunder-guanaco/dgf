from datetime import datetime
from django.forms import inlineformset_factory

from .models import Highlight, FavoriteCourse, Friend, DiscInBag, Ace, Video
from .widgets import AlreadyFetchedObjectsSelect, PartialDateWidget, ALL_DISCS, ALL_COURSES


def favorite_course_formset_factory():
    return inlineformset_factory(
        Friend, FavoriteCourse, fields=('course',),
        max_num=5, extra=5, validate_max=True, widgets={
            'course': AlreadyFetchedObjectsSelect(available_options=ALL_COURSES)
        }
    )


def highlight_formset_factory():
    return inlineformset_factory(
        Friend, Highlight, fields=('content',),
        max_num=5, extra=5, validate_max=True
    )


def disc_formset_factory():
    return inlineformset_factory(
        Friend, DiscInBag, fields=('type', 'amount', 'disc'),
        extra=1, widgets={
            'disc': AlreadyFetchedObjectsSelect(available_options=ALL_DISCS,
                                                attrs={'class': 'chosen-select'})
        }
    )


def ace_formset_factory():
    current_year = datetime.now().year
    return inlineformset_factory(
        Friend, Ace, fields=('friend', 'disc', 'course', 'hole', 'type', 'date'),
        extra=0, widgets={
            'date': PartialDateWidget(years=range(current_year, current_year - 20, -1)),
            'disc': AlreadyFetchedObjectsSelect(available_options=ALL_DISCS),
            'course': AlreadyFetchedObjectsSelect(available_options=ALL_COURSES)
        }
    )


def video_formset_factory():
    return inlineformset_factory(
        Friend, Video, fields=('url', 'type'),
        extra=0
    )
