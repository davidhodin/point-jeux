from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'informations.views.accueil'),
	url(r'^regles/$', 'informations.views.regles'),
	url(r'^configuration/$', 'informations.views.configuration'),
	url(r'^accueil/$', 'informations.views.accueil'),
	)
