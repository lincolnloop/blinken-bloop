from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^accounts/', include('authtools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('events.urls', namespace='events')),
)
