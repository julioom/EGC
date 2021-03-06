from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^crearCSVandIndex', 'main.views.crearCSV'),
    url(r'^populate', 'main.views.populateDB'),
    url(r'^loadRS', 'main.views.loadRS'),
    url(r'^searchGenreWhoosh', 'main.views.searchByGenre'),
    url(r'^searchGenreDjango', 'main.views.peliculas_por_genero'),
    url(r'^searchSynopsis', 'main.views.searchBySynopsis'),
    url(r'^searchUser', 'main.views.searchByUser'),
    url(r'^recommendedFilmsByFilm', 'main.views.recommendedFilms'),
       url(r'^recommendedFilmsByUser', 'main.views.recommendedFilms2'),
    url(r'^similarFilms', 'main.views.similarFilms'),
) + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
