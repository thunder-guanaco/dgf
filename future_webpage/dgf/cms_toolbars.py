from cms.utils.urlutils import admin_reverse
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool


class FriendsToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'dgf-friends',
            'Friends',
        )
        menu.add_sideframe_item(
            name='Friends List',
            url=admin_reverse('dgf_friend_changelist'),
        )
        menu.add_modal_item(
            name='New Friend',
            url=admin_reverse('dgf_friend_add'),
        )
        
toolbar_pool.register(FriendsToolbar)
