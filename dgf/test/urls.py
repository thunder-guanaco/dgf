from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^friends/', include('dgf.urls')),
    re_path(r'', include('cms.urls')),
    path('cookies/', include('cookie_consent.urls')),
]
