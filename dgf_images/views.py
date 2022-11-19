from django.views.generic import DetailView, ListView

from dgf.models import Friend
from dgf_images.models import ImageGenerator


class IndexView(ListView):
    queryset = ImageGenerator.objects.filter(active=True)
    context_object_name = 'image_generators'
    template_name = 'dgf_images/list.html'


class DetailView(DetailView):
    model = ImageGenerator
    context_object_name = 'image_generator'
    slug_field = 'slug'
    extra_context = {'friends': Friend.objects.all()}

    def get_template_names(self):
        return f'dgf_images/generators/{self.object.slug}.html'
