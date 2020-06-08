from django.forms import SelectDateWidget, Select
from partial_date import PartialDate

from .models import Disc, Course


def all_objects(object_type):
    return [('', '---')] + [(x.id, str(x)) for x in
                            object_type.objects.all().order_by('id')]


ALL_COURSES = all_objects(Course)
ALL_DISCS = all_objects(Disc)


class AlreadyFetchedObjectsSelect(Select):

    def __init__(self, available_options=(), *args, **kwargs):
        self.all_fetched_options = available_options
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        self.choices = self.all_fetched_options
        return super().get_context(name, value, attrs)


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
