from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'rami.views.partiesRami'),
	url(r'^partiesRami/$', 'rami.views.partiesRami'),
	url(r'^selectPartie/(?P<partie>\d+)/$', 'rami.views.selectPartie'),
	url(r'^encoursRami/$', 'rami.views.encoursRami'),
	url(r'^newRami/$', 'rami.views.newRami'),
	url(r'^suprimeRami/(?P<mene>\d+)/$', 'rami.views.suprimePartie'),
	)
