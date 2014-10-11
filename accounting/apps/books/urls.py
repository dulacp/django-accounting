from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.DashboardView.as_view(),
        name="dashboard"),

    # Organizations
    url(r'^organizations/$',
        views.OrganizationListView.as_view(),
        name="organization-list"),
    url(r'^organizations/create/$',
        views.OrganizationCreateView.as_view(),
        name="organization-create"),
)
