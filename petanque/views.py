#-*- coding: utf-8 -*-
from django.shortcuts import render
from petanque.models import PartiePetanque, MenePartiePetanque
from django.shortcuts import redirect
# Imports de App Engine
from google.appengine.api import users
from google.appengine.ext import ndb


def partiesPetanque(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Sélectionne toutes les parties
		parties = PartiePetanque.query(ancestor=ndb.Key("User", user.nickname())).order(-PartiePetanque.datePartie).fetch()
		if parties == None:
			return render(request, 'startPetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'parties': None, 'message': True })
		else:
			return render(request, 'startPetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'parties': parties, 'message': False })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def selectPartie(request, partie=0):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Sélectionne la partie
		request.session['partiePetanque'] = partie
		# Récupère la partie en cours
		partieEnCours = PartiePetanque.get_by_id(int(partie), parent=ndb.Key("User", user.nickname()))
		keyPartieEnCours = partieEnCours.key
		# Récupère les mènes de la partie
		menesEnCours = MenePartiePetanque.query(ancestor=keyPartieEnCours).order(MenePartiePetanque.datePartie).fetch()
		# Retourne à la page de la partie en cours
		return render(request, 'petanque/partiePetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partieEnCours, 'menes': menesEnCours })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def encoursPetanque(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# vérifie si une partie est sélectionnée
		if request.session.get('partiePetanque', False):
			# Propose d'ajouter une nouvelle mène
			partie = PartiePetanque.get_by_id(int(request.session.get('partiePetanque')), parent=ndb.Key("User", user.nickname()))
			if request.method == "POST":
				# Calcule points équipes
				pointsEquipe1 = 0
				pointsEquipe2 = 0
				# Points de base
				if request.POST["preneur"] == 'equipe1':
					pointsEquipe1 = int(request.POST["points"])
				else:
					pointsEquipe2 = int(request.POST["points"])
				# Ajout de la mène
				nouvelleMene = MenePartiePetanque(parent = partie.key, pointsEquipe1 = pointsEquipe1, pointsEquipe2 = pointsEquipe2)
				nouvelleMene.put()
				# modification de la partie
				partie.pointsEquipe1 = partie.pointsEquipe1 + nouvelleMene.pointsEquipe1
				partie.pointsEquipe2 = partie.pointsEquipe2 + nouvelleMene.pointsEquipe2
				partie.nombreMenes = partie.nombreMenes + 1
				# Teste si la partie est terminée
				fini = False
				if partie.pointsEquipe1 >= partie.fintypeParite:
					partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe1
					fini = True
				if partie.pointsEquipe2 >= partie.fintypeParite:
					partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe2
					fini = True
				partie.put()
			# Récupère les mènes de la partie
			menesEnCours = MenePartiePetanque.query(ancestor=partie.key).order(MenePartiePetanque.datePartie).fetch()
			return render(request, 'petanque/partiePetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partie, 'menes': menesEnCours })
		else:
			# Aucune partie n'a été sélectionnée
			return render(request, 'petanque/partiePetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': True, 'partie': None, 'menes': None })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def newPetanque(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		if request.method == "POST":
			# Enregistrement des noms d'équipes
			if request.POST["equipe1"] == "":
				nomEquipe1 = 'Equipe 1'
			else:
				nomEquipe1 = request.POST["equipe1"]
			if request.POST["equipe2"] == "":
				nomEquipe2 = 'Equipe 2'
			else:
				nomEquipe2 = request.POST["equipe2"]
			nouvellePartie = PartiePetanque(parent=ndb.Key("User", user.nickname()), statusPartie = 'En cours...', nomEquipe1 = nomEquipe1, nomEquipe2 = nomEquipe2, typePartie = request.POST['typePartie'])
			key = nouvellePartie.put()
			request.session['partiePetanque'] = key.integer_id()
			return render(request, 'petanque/partiePetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': nouvellePartie, 'menes': None })
		else:
			return render(request, 'petanque/newPetanque.html', { 'urlconnecte': users.create_logout_url('/') })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def suprimePartie(request, mene = 0):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Retourne à la page de la partie en cours
		partieActuelle = PartiePetanque.get_by_id(int(request.session.get('partiePetanque')), parent=ndb.Key("User", user.nickname()))
		try:
			# Récupère la mène en cours
			meneEnCours = MenePartiePetanque.get_by_id(int(mene), parent=partieActuelle.key)
			# Mise à jour de la partie
			partieActuelle.pointsEquipe1 = partieActuelle.pointsEquipe1 - meneEnCours.pointsEquipe1
			partieActuelle.pointsEquipe2 = partieActuelle.pointsEquipe2 - meneEnCours.pointsEquipe2
			partieActuelle.nombreMenes = partieActuelle.nombreMenes - 1
			# Suppression de la mene
			meneEnCours.key.delete()
			partieActuelle.put()
		except:
			print "Erreur de suppression de la partie"
		# Récupère les mènes de la partie
		menesEnCours = MenePartiePetanque.query(ancestor=partieActuelle.key).order(MenePartiePetanque.datePartie).fetch()
		return render(request, 'petanque/partiePetanque.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partieActuelle, 'menes': menesEnCours })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

