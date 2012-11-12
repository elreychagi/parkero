from django.conf.urls import patterns, include, url
from dalero import settings

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin

#admin.autodiscover()
from dalero.settings import STATIC_ROOT

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home', name='home'),
    url(r'^users/', include('users.urls')),
    url(r'^app/', include('website.app_urls')),
    url(r'^geo/', include('geo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT,
                                                                   'show_indexes': True}),
    )