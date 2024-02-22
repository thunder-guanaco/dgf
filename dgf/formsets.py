from datetime import datetime

from django.forms import inlineformset_factory

from dgf.models import Highlight, FavoriteCourse, Friend, DiscInBag, Ace, Video, Disc, Course, Sponsor
from dgf.widgets import AlreadyFetchedObjectsSelect, PartialDateWidget


def all_objects(object_type, order_by):
    return [('', '---')] + [(x.id, str(x)) for x in
                            object_type.objects.all().order_by(order_by)]


def all_courses():
    return all_objects(Course, 'name')


ALL_DISCS = all_objects(Disc, 'mold')


def favorite_course_formset_factory():
    return inlineformset_factory(
        Friend, FavoriteCourse, fields=('course',),
        max_num=5, extra=5, validate_max=True
    )


def highlight_formset_factory():
    return inlineformset_factory(
        Friend, Highlight, fields=('content',),
        max_num=10, extra=10, validate_max=True
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
            'course': AlreadyFetchedObjectsSelect(available_options=all_courses())
        }
    )


def video_formset_factory():
    return inlineformset_factory(
        Friend, Video, fields=('url', 'type'),
        extra=0
    )


def sponsors_formset_factory():
    return inlineformset_factory(
        Friend, Sponsor, fields=('name', 'link', 'logo'),
        max_num=3, extra=3, validate_max=True, can_delete=False
    )
