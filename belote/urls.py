from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'belote.views.partiesBelote'),
	url(r'^partiesBelote/$', 'belote.views.partiesBelote'),
	url(r'^selectPartie/(?P<partie>\d+)/$', 'belote.views.selectPartie'),
	url(r'^encoursBelote/$', 'belote.views.encoursBelote'),
	url(r'^newBelote/$', 'belote.views.newBelote'),
	url(r'^suprimeBelote/(?P<mene>\d+)/$', 'belote.views.suprimePartie'),
	)
