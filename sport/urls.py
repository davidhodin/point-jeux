from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sport.views.home', name='home'),
    url(r'^belote/', include('belote.urls')),
    url(r'^petanque/', include('petanque.urls')),
    url(r'^tarot/', include('tarot.urls')),
    url(r'^rami/', include('rami.urls')),
    url(r'^informations/', include('informations.urls')),
    # Liste des liens de la page principale
    url(r'^$', 'sport.views.start'),
)
