#-*- coding: utf-8 -*-
from django.shortcuts import render
from belote.models import PartieBelotte, MenePartieBelotte
from django.shortcuts import redirect
# Imports de App Engine
from google.appengine.api import users
from google.appengine.ext import ndb

def partiesBelote(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Sélectionne toutes les parties
		parties = PartieBelotte.query(ancestor=ndb.Key("User", user.nickname())).order(-PartieBelotte.datePartie).fetch()
		if parties == None:
			return render(request, 'startBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'parties': None, 'message': True })
		else:
			return render(request, 'startBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'parties': parties, 'message': False })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def selectPartie(request, partie=0):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Sélectionne la partie
		request.session['partieBelote'] = partie
		# Récupère la partie en cours
		partieEnCours = PartieBelotte.get_by_id(int(partie), parent=ndb.Key("User", user.nickname()))
		keyPartieEnCours = partieEnCours.key
		# Récupère les mènes de la partie
		menesEnCours = MenePartieBelotte.query(ancestor=keyPartieEnCours).order(MenePartieBelotte.datePartie).fetch()
		# Retourne à la page de la partie en cours
		return render(request, 'belote/partieBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partieEnCours, 'menes': menesEnCours })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri())})

def encoursBelote(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# vérifie si une partie est sélectionnée
		if request.session.get('partieBelote', False):
			# Propose d'ajouter une nouvelle mène
			partie = PartieBelotte.get_by_id(int(request.session.get('partieBelote')), parent=ndb.Key("User", user.nickname()))
			if request.method == "POST":
				# Calcule points équipes
				pointsEquipe1 = 0
				pointsEquipe2 = 0
				beloteEquipe1 = 0
				BelEquipe1 = False
				beloteEquipe2 = 0
				BelEquipe2 = False
				annonceEquipe1 = 0
				annonceEquipe2 = 0
				# Récupère litige
				litige = partie.litigeDernierePartie
				# Récupère les points réalisés
				if request.POST["compte"] == 'equipe1':
					pointsEqui1 = int(request.POST["points"])
					pointsEqui2 = 162 - int(request.POST["points"])
				else:
					pointsEqui2 = int(request.POST["points"])
					pointsEqui1 = 162 - int(request.POST["points"])
				# Pointes de la belote
				if request.POST["belote"] == 'Equipe1':
					beloteEquipe1 = 20
					BelEquipe1 = True
				elif request.POST["belote"] == 'Equipe2':
					beloteEquipe2 = 20
					BelEquipe2 = True
				# points de l'annonce
				if request.POST["annonce"] == 'equipe1':
					annonceEquipe1 = int(request.POST["pointsAnnonce"])
				else:
					annonceEquipe2 = int(request.POST["pointsAnnonce"])
				# Points de base
				if request.POST["preneur"] == 'equipe1':
					if (pointsEqui1 + beloteEquipe1 + annonceEquipe1) < (pointsEqui2 + beloteEquipe2 + annonceEquipe2):
						print "Perdu equipe 1"
						pointsEquipe1 = beloteEquipe1 
						pointsEquipe2 = 162 + beloteEquipe2 + litige + annonceEquipe2 + annonceEquipe1
						partie.litigeDernierePartie = 0
					elif (pointsEqui1 + beloteEquipe1 + annonceEquipe1) > (pointsEqui2 + beloteEquipe2 + annonceEquipe2):
						if pointsEqui1 == 162:
							print "capot equipe 1"
							pointsEquipe1 = 252 + beloteEquipe1 + litige + annonceEquipe1 + annonceEquipe2
							pointsEquipe2 = beloteEquipe2
							partie.litigeDernierePartie = 0
						else:
							print "Gagnée equipe 1"
							pointsEquipe1 = pointsEqui1 + beloteEquipe1 + litige + annonceEquipe1
							pointsEquipe2 = pointsEqui2 + beloteEquipe2 + annonceEquipe2
							partie.litigeDernierePartie = 0
					else:
						print "litige equipe 1"
						pointsEquipe1 = beloteEquipe1
						pointsEquipe2 = pointsEqui2 + beloteEquipe2 + annonceEquipe2
						partie.litigeDernierePartie = partie.litigeDernierePartie + pointsEqui1 + annonceEquipe1
				else:
					if (pointsEqui2 + beloteEquipe2 + annonceEquipe2) < (pointsEqui1 + beloteEquipe1 + annonceEquipe1):
						print "Perdu equipe 2"
						pointsEquipe2 = beloteEquipe2
						pointsEquipe1 = 162 + beloteEquipe1 + litige + annonceEquipe1 + annonceEquipe2
						partie.litigeDernierePartie = 0
					elif (pointsEqui2 + beloteEquipe2 + annonceEquipe2) > (pointsEqui1 + beloteEquipe1 + annonceEquipe1):
						if pointsEqui2 == 162:
							print "capot equipe 2"
							pointsEquipe2 = 252 + beloteEquipe2 + litige + annonceEquipe2 + annonceEquipe1
							pointsEquipe1 = beloteEquipe1
							partie.litigeDernierePartie = 0
						else:
							print "Gagnée equipe 2"
							pointsEquipe2 = pointsEqui2 + beloteEquipe2 + litige + annonceEquipe2
							pointsEquipe1 = pointsEqui1 + beloteEquipe1 + annonceEquipe1
							partie.litigeDernierePartie = 0
					else:
						print "litige equipe 2"
						pointsEquipe2 = beloteEquipe2
						pointsEquipe1 = pointsEqui1 + beloteEquipe1 + annonceEquipe1
						partie.litigeDernierePartie = partie.litigeDernierePartie + pointsEqui2 + annonceEquipe2
				# Ajout de la mène
				nouvelleMene = MenePartieBelotte(parent = partie.key, pointsEquipe1 = pointsEquipe1, pointsEquipe2 = pointsEquipe2, beloteEquipe1 = BelEquipe1, beloteEquipe2 = BelEquipe2)
				nouvelleMene.put()
				# modification de la partie
				partie.pointsEquipe1 = partie.pointsEquipe1 + pointsEquipe1
				partie.pointsEquipe2 = partie.pointsEquipe2 + pointsEquipe2
				partie.nombreMenes = partie.nombreMenes + 1
				# Teste si la partie est terminée
				fini = False
				if partie.typePartie == 'parties':
					if partie.nombreMenes == partie.fintypeParite:
						if partie.pointsEquipe1 > partie.pointsEquipe2:
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe1
							fini = True
						else:
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe2
							fini = True
				else:
					if partie.pointsEquipe1 > partie.fintypeParite:
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe1
						fini = True
					if partie.pointsEquipe2 > partie.fintypeParite:
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe2
						fini = True
				partie.put()
			# Récupère les mènes de la partie
			menesEnCours = MenePartieBelotte.query(ancestor=partie.key).order(MenePartieBelotte.datePartie).fetch()
			return render(request, 'belote/partieBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partie, 'menes': menesEnCours })
		else:
			# Aucune partie n'a été sélectionnée
			return render(request, 'belote/partieBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': True, 'partie': None, 'menes': None })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def newBelote(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		if request.method == "POST":
			if request.POST['typePartie'] == 'parties':
				typePartie = 'parties'
				fintypeParite = int(request.POST['parties'])
			else:
				typePartie = 'points'
				fintypeParite = int(request.POST['points'])
			if request.POST["equipe1"] == "":
				nomEquipe1 = 'Equipe 1'
			else:
				nomEquipe1 = request.POST["equipe1"]
			if request.POST["equipe2"] == "":
				nomEquipe2 = 'Equipe 2'
			else:
				nomEquipe2 = request.POST["equipe2"]
			# Crée la nouvelle partie
			nouvellePartie = PartieBelotte(parent=ndb.Key("User", user.nickname()), statusPartie = 'En cours...', nomEquipe1 = nomEquipe1, nomEquipe2 = nomEquipe2, typePartie = typePartie, fintypeParite = int(fintypeParite))
			key = nouvellePartie.put()
			request.session['partieBelote'] = key.integer_id()
			# Retourne à la page de la partie en cours
			return render(request, 'belote/partieBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': nouvellePartie, 'menes': None })
		else:
			return render(request, 'belote/newBelote.html', { 'urlconnecte': users.create_logout_url('/') })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri())})

def suprimePartie(request, mene = 0):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Retourne à la page de la partie en cours
		partieActuelle = PartieBelotte.get_by_id(int(request.session.get('partieBelote')), parent=ndb.Key("User", user.nickname()))
		try:
			# Récupère la mène en cours
			meneEnCours = MenePartieBelotte.get_by_id(int(mene), parent=partieActuelle.key)
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
		menesEnCours = MenePartieBelotte.query(ancestor=partieActuelle.key).order(MenePartieBelotte.datePartie).fetch()
		return render(request, 'belote/partieBelote.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partieActuelle, 'menes': menesEnCours })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri())})
