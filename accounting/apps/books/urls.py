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
    url(r'^organizations/(?P<pk>\d)/edit/$',
        views.OrganizationUpdateView.as_view(),
        name="organization-edit"),
    url(r'^organizations/(?P<pk>\d)/detail/$',
        views.OrganizationDetailView.as_view(),
        name="organization-detail"),

    # Invoices
    url(r'^invoice/$',
        views.InvoiceListView.as_view(),
        name="invoice-list"),
    url(r'^invoice/create/$',
        views.InvoiceCreateView.as_view(),
        name="invoice-create"),
    url(r'^invoice/(?P<pk>\d)/edit/$',
        views.InvoiceUpdateView.as_view(),
        name="invoice-edit"),
)
