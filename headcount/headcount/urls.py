from django.conf.urls import patterns, include, url
from django.contrib import admin

from events.views import CustomLogoutView

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^accounts/logout/$', CustomLogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('authtools.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('events.urls', namespace='events')),
)
