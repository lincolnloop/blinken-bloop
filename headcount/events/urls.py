from django.conf.urls import patterns, url

from .views import Dashboard


urlpatterns = patterns(
    '',
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
)
