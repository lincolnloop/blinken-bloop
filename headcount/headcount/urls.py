from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^accounts/logout/$', views.CustomLogoutView.as_view(),
        name='logout'),
    url(r'^accounts/login/$', views.CustomLoginView.as_view(),
        name='login'),
    url(r'^accounts/signup/$', views.RegisterView.as_view(),
        name='register'),
    url(r'^accounts/', include('authtools.urls', namespace='accounts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('events.urls', namespace='events')),
)
