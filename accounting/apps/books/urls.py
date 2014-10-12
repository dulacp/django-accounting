from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$',
        views.DashboardView.as_view(),
        name="dashboard"),

    # Organizations
    url(r'^organization/$',
        views.OrganizationListView.as_view(),
        name="organization-list"),
    url(r'^organization/create/$',
        views.OrganizationCreateView.as_view(),
        name="organization-create"),
    url(r'^organization/(?P<pk>\d)/edit/$',
        views.OrganizationUpdateView.as_view(),
        name="organization-edit"),
    url(r'^organization/(?P<pk>\d)/detail/$',
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

    # Invoices
    url(r'^bill/$',
        views.BillListView.as_view(),
        name="bill-list"),
    url(r'^bill/create/$',
        views.BillCreateView.as_view(),
        name="bill-create"),
    url(r'^bill/(?P<pk>\d)/edit/$',
        views.BillUpdateView.as_view(),
        name="bill-edit"),
)
