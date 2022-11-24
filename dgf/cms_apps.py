from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class FriendsApphook(CMSApp):
    app_name = 'dgf'
    name = 'Friends Application'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['dgf.urls']


@apphook_pool.register
class CookiesApphook(CMSApp):
    app_name = 'cookie_contents'
    name = 'Cookie Consents Application'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['cookie_consent.urls']


@apphook_pool.register
class ImagesApphook(CMSApp):
    app_name = 'dgf_images'
    name = 'Images Application'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['dgf_images.urls']
