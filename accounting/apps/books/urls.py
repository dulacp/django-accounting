from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.OrganizationListView.as_view(),
        name="organization-list"),
)
