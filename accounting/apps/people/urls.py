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
    url(r'^client/(?P<pk>\d+)/edit/$',
        views.ClientUpdateView.as_view(),
        name="client-edit"),
    url(r'^client/(?P<pk>\d+)/detail/$',
        views.ClientDetailView.as_view(),
        name="client-detail"),

    # Employees
    url(r'^employee/$',
        views.EmployeeListView.as_view(),
        name="employee-list"),
    url(r'^employee/create/$',
        views.EmployeeCreateView.as_view(),
        name="employee-create"),
    url(r'^employee/(?P<pk>\d+)/edit/$',
        views.EmployeeUpdateView.as_view(),
        name="employee-edit"),
    url(r'^employee/(?P<pk>\d+)/detail/$',
        views.EmployeeDetailView.as_view(),
        name="employee-detail"),
)
