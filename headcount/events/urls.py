from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.EventWizard.as_view(), name='home'),
    url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
    url(r'^event/new/$', views.CreateEvent.as_view(), name='create'),
    url(r'^event/edit/(?P<slug>\w+)/$', views.UpdateEvent.as_view(),
        name='edit'),
    url(r'^event/delete/(?P<slug>\w+)/$', views.DeleteEvent.as_view(),
        name='delete'),
    url(r'event/rsvp/(?P<slug>\w+)/$', views.EventDetailRSVP.as_view(),
        name='rsvp'),
    url(r'event/detail/(?P<slug>\w+)/$', views.EventDetail.as_view(),
        name='detail'),
    url(r'event/(?P<slug>\w+)/rsvp/update/$', views.RSVPUpdate.as_view(),
        name='update_rsvp'),
)
