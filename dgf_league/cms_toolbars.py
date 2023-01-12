from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.utils.translation import gettext_lazy as _


class LeagueToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'dgf-league',
            _('League'),
        )
        menu.add_sideframe_item(
            name=_('Teams'),
            url=admin_reverse('dgf_league_team_changelist'),
        )
        menu.add_sideframe_item(
            name=_('Add team'),
            url=admin_reverse('dgf_league_team_add'),
        )


toolbar_pool.register(LeagueToolbar)
