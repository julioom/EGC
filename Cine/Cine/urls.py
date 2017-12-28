from django.conf.urls import patterns, include, url
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Cine.views.home', name='home'),
    # url(r'^Cine/', include('Cine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.index'),
    url(r'^populate', 'main.views.crearCSV'),
    url(r'^populate', 'main.views.populateDB'),
    url(r'^loadRS', 'main.views.loadRS'),
    url(r'^search', 'main.views.search'),
    url(r'^recommendedFilms', 'main.views.recommendedFilms'),
    url(r'^similarFilms', 'main.views.similarFilms'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
