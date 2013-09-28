from django.conf.urls import patterns, url

from .views import Dashboard, Home


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
)
