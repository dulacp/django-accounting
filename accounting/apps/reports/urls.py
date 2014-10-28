from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

    # Reports
    url(r'^report/$',
        views.ReportListView.as_view(),
        name="report-list"),
    url(r'^report/tax/$',
        views.TaxReportView.as_view(),
        name="tax-report"),

    # Settings
    url(r'^settings/$',
        views.SettingsListView.as_view(),
        name="settings-list"),
    url(r'^settings/financial/$',
        views.FinancialSettingsUpdateView.as_view(),
        name="settings-financial"),
)
