from cms.api import add_plugin
from cms.models import Placeholder
from django.test import TestCase
from parameterized import parameterized

from ...cms_plugins import FriendPluginPublisher, FriendsHeaderPluginPublisher
from ...models import Friend


class DgfPluginsTests(TestCase):

    @parameterized.expand([
        (FriendPluginPublisher, lambda context: context['friend']),
        (FriendsHeaderPluginPublisher, lambda context: context['friends'][0]),
    ])
    def test_friend_plugin(self, plugin_class, how_to_get_a_friend):
        friend, _ = Friend.objects.get_or_create(defaults={'username': 'test'})
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            plugin_class,
            'en',
            target=None,
            friend=friend
        )

        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertEqual(how_to_get_a_friend(context).username, 'test')
