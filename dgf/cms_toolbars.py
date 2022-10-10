from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from filer.models.foldermodels import Folder


class FriendsToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'dgf-friends',
            _('Friends'),
        )
        menu.add_sideframe_item(
            name=_('Bag tag changes'),
            url=admin_reverse('dgf_bagtagchange_changelist'),
        )
        menu.add_sideframe_item(
            name=_('All friends'),
            url=admin_reverse('dgf_friend_changelist'),
        )
        menu.add_modal_item(
            name=_('New friend'),
            url=admin_reverse('dgf_friend_add'),
        )


class CourseToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'dgf-course',
            _('Courses'),
        )
        menu.add_sideframe_item(
            name=_('All courses'),
            url=admin_reverse('dgf_course_changelist'),
        )
        menu.add_modal_item(
            name=_('New course'),
            url=admin_reverse('dgf_course_add'),
        )


class TournamentToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'dgf-tournament',
            _('Tournaments'),
        )
        menu.add_sideframe_item(
            name=_('All tours'),
            url=admin_reverse('dgf_tour_changelist'),
        )
        menu.add_sideframe_item(
            name=_('All tournaments'),
            url=admin_reverse('dgf_tournament_changelist'),
        )
        menu.add_modal_item(
            name=_('New tournament'),
            url=admin_reverse('dgf_tournament_add'),
        )


class FolderToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            'filer-folder',
            _('Folders'),
        )
        menu.add_sideframe_item(
            name=_('All folders'),
            url=admin_reverse('filer_folder_changelist'),
        )
        background_folder, __ = Folder.objects.get_or_create(name=settings.BACKGROUND_FOLDER)
        menu.add_sideframe_item(
            name=_(background_folder.name),
            url=admin_reverse('filer-directory_listing', args=(background_folder.id,)),
        )


toolbar_pool.register(FriendsToolbar)
toolbar_pool.register(CourseToolbar)
toolbar_pool.register(TournamentToolbar)
toolbar_pool.register(FolderToolbar)
