from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import re_path

urlpatterns = [
    re_path(r'^friends/', include('dgf.urls')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^cookies/', include('cookie_consent.urls')),
    re_path(r'^', include('cms.urls')),
]
