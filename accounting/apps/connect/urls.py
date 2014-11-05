from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

    url(r'^$',
        views.RootRedirectionView.as_view(),
        name="root"),

    # Step by step
    url(r'^getting-started/$',
        views.GettingStartedView.as_view(),
        name="getting-started")
)
