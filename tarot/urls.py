from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'tarot.views.partiesTarot'),
	url(r'^partiesTarot/$', 'tarot.views.partiesTarot'),
	url(r'^selectPartie/(?P<partie>\d+)/$', 'tarot.views.selectPartie'),
	url(r'^encoursTarot/$', 'tarot.views.encoursTarot'),
	url(r'^newTarot/$', 'tarot.views.newTarot'),
	url(r'^suprimeTarot/(?P<mene>\d+)/$', 'tarot.views.suprimePartie'),
	)
