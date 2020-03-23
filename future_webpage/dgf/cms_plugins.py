from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from .models import FriendPluginModel, Friend


@plugin_pool.register_plugin
class FriendPluginPublisher(CMSPluginBase):
    model = FriendPluginModel
    module = _("Disc Golf Friends")
    name = _("Friend")
    render_template = "dgf/friend_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context


@plugin_pool.register_plugin
class FriendsHeaderPluginPublisher(CMSPluginBase):
    model = FriendPluginModel
    module = _("Disc Golf Friends")
    name = _("Friends Header")
    render_template = "dgf/friends_header.html"

    def render(self, context, instance, placeholder):
        context.update({'friends': Friend.objects.all()})
        print(context)
        return context
