from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class FriendsApphook(CMSApp):
    app_name = "dgf"
    name = "Friends Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["dgf.urls"]
