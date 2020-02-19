from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import FriendPluginModel
from django.utils.translation import ugettext as _


@plugin_pool.register_plugin
class FriendPluginPublisher(CMSPluginBase):
    model = FriendPluginModel
    module = _("Disc Golf Friends")
    name = _("Friend")
    render_template = "dgf/friend_plugin.html"

    def render(self, context, instance, placeholder):
        context.update({'instance': instance})
        return context