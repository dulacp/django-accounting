from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

    # Clients
    url(r'^client/$',
        views.ClientListView.as_view(),
        name="client-list"),
    url(r'^client/create/$',
        views.ClientCreateView.as_view(),
        name="client-create"),
    url(r'^client/(?P<pk>\d)/edit/$',
        views.ClientUpdateView.as_view(),
        name="client-edit"),
    url(r'^client/(?P<pk>\d)/detail/$',
        views.ClientDetailView.as_view(),
        name="client-detail"),
)
