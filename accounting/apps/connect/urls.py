from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',

    url(r'^$',
        views.RootRedirectionView.as_view(),
        name="root"),

    # Step by step

)
