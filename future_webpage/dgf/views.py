from django.views import generic

from .models import Friend


class IndexView(generic.ListView):
    template_name = 'dgf/friend_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return Friend.objects.all()


class DetailView(generic.DetailView):
    model = Friend
    slug_field = 'slug'
    template_name = 'dgf/friend_detail.html'

    def get_queryset(self):
        return Friend.objects.all()


class UpdateView(generic.edit.UpdateView):
    model = Friend
    fields = ['username', 'first_name', 'last_name', 'nickname', 'pdga_number', 'city', 'main_photo']
    template_name_suffix = '_profile'

    def get_object(self, queryset=None):
        return self.request.user.friend
