from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'petanque.views.partiesPetanque'),
	url(r'^partiesPetanque/$', 'petanque.views.partiesPetanque'),
	url(r'^selectPartie/(?P<partie>\d+)/$', 'petanque.views.selectPartie'),
	url(r'^encoursPetanque/$', 'petanque.views.encoursPetanque'),
	url(r'^newPetanque/$', 'petanque.views.newPetanque'),
	url(r'^suprimePetanque/(?P<mene>\d+)/$', 'petanque.views.suprimePartie'),
	)
