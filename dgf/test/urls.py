from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^friends/', include('dgf.urls')),
    url(r'', include('cms.urls')),
]
