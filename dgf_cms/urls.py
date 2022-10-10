# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from dgf.handlers import server_error

admin.autodiscover()

urlpatterns = [
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

urlpatterns += i18n_patterns(
    re_path(r'^admin/', admin.site.urls),  # NOQA
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^cookies/', include('cookie_consent.urls')),
    re_path(r'^', include('cms.urls')),
    prefix_default_language=False
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
                      re_path(r'^mock/$', TemplateView.as_view(template_name='mock.html')),
                      re_path(r'^403/$', TemplateView.as_view(template_name='403.html')),
                      re_path(r'^404/$', TemplateView.as_view(template_name='404.html')),
                      re_path(r'^500/$', TemplateView.as_view(template_name='500.html')),
                      re_path(r'^media/(?P<path>.*)$', serve,
                              {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                  ] + staticfiles_urlpatterns() + urlpatterns

handler500 = server_error
