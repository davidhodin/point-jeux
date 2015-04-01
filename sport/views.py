#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from django.forms import ModelForm
from django.shortcuts import render
# Imports des modèles
from belote.models import PartieBelotte
from petanque.models import PartiePetanque
from tarot.models import PartieTarot
from rami.models import PartieRami
# Imports de App Engine
from google.appengine.api import users
from google.appengine.ext import ndb

def start(request):
	# Page d'accueil pour authentification
	user = users.get_current_user()
	# Vérifie si quelqu'un est déjà connecté
	if user:
		# Compte les parties
		partiesBelote = PartieBelotte.query(ancestor=ndb.Key("User", user.nickname())).count()
		partiesTarot = PartieTarot.query(ancestor=ndb.Key("User", user.nickname())).count()
		partiesPetanque = PartiePetanque.query(ancestor=ndb.Key("User", user.nickname())).count()
		partiesRami = PartieRami.query(ancestor=ndb.Key("User", user.nickname())).count()
		# Retourne la page d'accueil
		return render(request, 'startUtilisateur.html', { 'urlconnecte': users.create_logout_url('/'), 'username': user.nickname(), 'partiesBelote': partiesBelote, 'partiesTarot': partiesTarot, 'partiesPetanque': partiesPetanque, 'partiesRami': partiesRami })
	else:
		# Supprime toutes les parties en cours s'il y en a
		try:
			del request.session['partiePetanque']
		except KeyError:
			pass
		try:
			del request.session['partieTarot']
		except KeyError:
			pass
		try:
			del request.session['partieBelote']
		except KeyError:
			pass
		try:
			del request.session['partieRami']
		except KeyError:
			pass
		# Page d'accueil de base
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri())})
