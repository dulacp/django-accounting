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
    url(r'^report/profitloss/$',
        views.ProfitAndLossReportView.as_view(),
        name="profit-and-loss-report"),
    url(r'^report/payrun/$',
        views.PayRunReportView.as_view(),
        name="pay-run-report"),
    url(r'^report/invoicedetails/$',
        views.InvoiceDetailsView.as_view(),
        name="invoice-details-report"),

    # Settings
    url(r'^settings/$',
        views.SettingsListView.as_view(),
        name="settings-list"),
    url(r'^settings/business/$',
        views.BusinessSettingsUpdateView.as_view(),
        name="settings-business"),
    url(r'^settings/financial/$',
        views.FinancialSettingsUpdateView.as_view(),
        name="settings-financial"),
    url(r'^settings/payrun/$',
        views.PayRunSettingsUpdateView.as_view(),
        name="settings-payrun"),
)
