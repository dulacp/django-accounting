from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^books/', include('accounting.apps.books.urls', namespace="books")),
    url(r'^clients/', include('accounting.apps.clients.urls', namespace="clients")),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
