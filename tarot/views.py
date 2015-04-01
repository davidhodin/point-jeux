#-*- coding: utf-8 -*-
from django.shortcuts import render
from tarot.models import PartieTarot, MenePartieTarot
from django.shortcuts import redirect
# Imports de App Engine
from google.appengine.api import users
from google.appengine.ext import ndb

def partiesTarot(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Sélectionne toutes les parties
		parties = PartieTarot.query(ancestor=ndb.Key("User", user.nickname())).order(-PartieTarot.datePartie).fetch()
		if parties == None:
			return render(request, 'startTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'parties': None, 'message': True })
		else:
			return render(request, 'startTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'parties': parties, 'message': False })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def selectPartie(request, partie=0):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Sélectionne la partie
		request.session['partieTarot'] = partie
		# Récupère la partie en cours
		partieEnCours = PartieTarot.get_by_id(int(partie), parent=ndb.Key("User", user.nickname()))
		keyPartieEnCours = partieEnCours.key
		# Récupère les mènes de la partie
		menesEnCours = MenePartieTarot.query(ancestor=keyPartieEnCours).order(MenePartieTarot.datePartie).fetch()
		# Retourne à la page de la partie en cours
		return render(request, 'tarot/partieTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partieEnCours, 'menes': menesEnCours })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def encoursTarot(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# vérifie si une partie est sélectionnée
		if request.session.get('partieTarot', False):
			# Propose d'ajouter une nouvelle mène
			partie = PartieTarot.get_by_id(int(request.session.get('partieTarot')), parent=ndb.Key("User", user.nickname()))
			if request.method == "POST":
				# Calcule points équipes
				pointsEquipe1 = 0
				pointsEquipe2 = 0
				pointsEquipe3 = 0
				pointsEquipe4 = 0
				pointsEquipe5 = 0
				# Trois cas de partie possible
				if partie.nombreJoueurs == 3:
					# Récupère les informations
					preneur = request.POST["preneur"]
					contrat = int(request.POST["contrat"])
					bouts = int(request.POST["bouts"])
					points = int(request.POST["points"])
					chelem = int(request.POST["chelem"])
					petit = int(request.POST["petit"])
					poignee = int(request.POST["poignee"])
					pointsValide = 0
					if points >= bouts:
						pointsValide = (25 + (points - bouts)) * contrat + chelem + poignee + petit * contrat
						# Affectation des points
						if preneur == "equipe1":
							pointsEquipe1 = 2 * pointsValide
							pointsEquipe2 = -pointsValide
							pointsEquipe3 = -pointsValide
						elif preneur == "equipe2":
							pointsEquipe1 = - pointsValide
							pointsEquipe2 = 2 * pointsValide
							pointsEquipe3 = - pointsValide
						else:
							pointsEquipe1 = - pointsValide
							pointsEquipe2 = - pointsValide
							pointsEquipe3 = 2 * pointsValide
					else:
						pointsValide = (25 + (bouts - points)) * contrat + chelem + poignee - petit * contrat
						# Affectation des points
						if preneur == "equipe1":
							pointsEquipe1 = -2 * pointsValide
							pointsEquipe2 = pointsValide
							pointsEquipe3 = pointsValide
						elif preneur == "equipe2":
							pointsEquipe1 = pointsValide
							pointsEquipe2 = -2 * pointsValide
							pointsEquipe3 = pointsValide
						else:
							pointsEquipe1 = pointsValide
							pointsEquipe2 = pointsValide
							pointsEquipe3 = -2 * pointsValide
				elif partie.nombreJoueurs == 4:
					# Récupère les informations
					preneur = request.POST["preneur"]
					contrat = int(request.POST["contrat"])
					bouts = int(request.POST["bouts"])
					points = int(request.POST["points"])
					chelem = int(request.POST["chelem"])
					petit = int(request.POST["petit"])
					poignee = int(request.POST["poignee"])
					pointsValide = 0
					if points >= bouts:
						pointsValide = (25 + (points - bouts)) * contrat + chelem + poignee + petit * contrat
						# Affectation des points
						if preneur == "equipe1":
							pointsEquipe1 = 3 * pointsValide
							pointsEquipe2 = -pointsValide
							pointsEquipe3 = -pointsValide
							pointsEquipe4 = -pointsValide
						elif preneur == "equipe2":
							pointsEquipe1 = - pointsValide
							pointsEquipe2 = 3 * pointsValide
							pointsEquipe3 = - pointsValide
							pointsEquipe4 = - pointsValide
						elif preneur == "equipe3":
							pointsEquipe1 = - pointsValide
							pointsEquipe2 = - pointsValide
							pointsEquipe3 = 3 * pointsValide
							pointsEquipe4 = - pointsValide
						else:
							pointsEquipe1 = - pointsValide
							pointsEquipe2 = - pointsValide
							pointsEquipe3 = - pointsValide
							pointsEquipe4 = 3 * pointsValide
					else:
						pointsValide = (25 + (bouts - points)) * contrat + chelem + poignee - petit * contrat
						# Affectation des points
						if preneur == "equipe1":
							pointsEquipe1 = -3 * pointsValide
							pointsEquipe2 = pointsValide
							pointsEquipe3 = pointsValide
							pointsEquipe4 = pointsValide
						elif preneur == "equipe2":
							pointsEquipe1 = pointsValide
							pointsEquipe2 = -3 * pointsValide
							pointsEquipe3 = pointsValide
							pointsEquipe4 = pointsValide
						elif preneur == "equipe3":
							pointsEquipe1 = pointsValide
							pointsEquipe2 = pointsValide
							pointsEquipe3 = -3 * pointsValide
							pointsEquipe4 = pointsValide
						else :
							pointsEquipe1 = pointsValide
							pointsEquipe2 = pointsValide
							pointsEquipe3 = pointsValide
							pointsEquipe4 = -3 * pointsValide
				else :
					# Récupère les informations
					preneur = request.POST["preneur"]
					appele = request.POST["appele"]
					contrat = int(request.POST["contrat"])
					bouts = int(request.POST["bouts"])
					points = int(request.POST["points"])
					chelem = int(request.POST["chelem"])
					petit = int(request.POST["petit"])
					poignee = int(request.POST["poignee"])
					pointsValide = 0
					if points >= bouts:
						pointsValide = (25 + (points - bouts)) * contrat + chelem + poignee + petit * contrat
						# Affectation des points
						# points du preneur
						if preneur == "equipe1":
							pointsEquipe1 = 2 * pointsValide
						elif preneur == "equipe2":
							pointsEquipe2 = 2 * pointsValide
						elif preneur == "equipe3":
							pointsEquipe3 = 2 * pointsValide
						elif preneur == "equipe4":
							pointsEquipe4 = 2 * pointsValide
						else:
							pointsEquipe5 = 2 * pointsValide
						# points de l'appelé
						if appele == "equipe1":
							pointsEquipe1 = pointsEquipe1 + pointsValide
						elif appele == "equipe2":
							pointsEquipe2 = pointsEquipe2 + pointsValide
						elif appele == "equipe3":
							pointsEquipe3 = pointsEquipe3 + pointsValide
						elif appele == "equipe4":
							pointsEquipe4 = pointsEquipe4 + pointsValide
						else:
							pointsEquipe5 = pointsEquipe5 + pointsValide
						# points des autres joueurs
						if pointsEquipe1 == 0:
							pointsEquipe1 = - pointsValide
						if pointsEquipe2 == 0:
							pointsEquipe2 = - pointsValide
						if pointsEquipe3 == 0:
							pointsEquipe3 = - pointsValide
						if pointsEquipe4 == 0:
							pointsEquipe4 = - pointsValide
						if pointsEquipe5 == 0:
							pointsEquipe5 = - pointsValide
					else:
						pointsValide = (25 + (bouts - points)) * contrat + chelem + poignee - petit * contrat
						# Affectation des points
						# points du preneur
						if preneur == "equipe1":
							pointsEquipe1 = -2 * pointsValide
						elif preneur == "equipe2":
							pointsEquipe2 = -2 * pointsValide
						elif preneur == "equipe3":
							pointsEquipe3 = -2 * pointsValide
						elif preneur == "equipe4":
							pointsEquipe4 = -2 * pointsValide
						else:
							pointsEquipe5 = -2 * pointsValide
						# points de l'appelé
						if preneur == appele:
							if appele == "equipe1":
								pointsEquipe1 = pointsEquipe1 - 2 * pointsValide
							elif appele == "equipe2":
								pointsEquipe2 = pointsEquipe2 - 2 * pointsValide
							elif appele == "equipe3":
								pointsEquipe3 = pointsEquipe3 - 2 * pointsValide
							elif appele == "equipe4":
								pointsEquipe4 = pointsEquipe4 - 2 * pointsValide
							else:
								pointsEquipe5 = pointsEquipe5 - 2 * pointsValide	
						else:
							if appele == "equipe1":
								pointsEquipe1 = pointsEquipe1 - pointsValide
							elif appele == "equipe2":
								pointsEquipe2 = pointsEquipe2 - pointsValide
							elif appele == "equipe3":
								pointsEquipe3 = pointsEquipe3 - pointsValide
							elif appele == "equipe4":
								pointsEquipe4 = pointsEquipe4 - pointsValide
							else:
								pointsEquipe5 = pointsEquipe5 - pointsValide
						# points des autres joueurs
						if pointsEquipe1 == 0:
							pointsEquipe1 = pointsValide
						if pointsEquipe2 == 0:
							pointsEquipe2 = pointsValide
						if pointsEquipe3 == 0:
							pointsEquipe3 = pointsValide
						if pointsEquipe4 == 0:
							pointsEquipe4 = pointsValide
						if pointsEquipe5 == 0:
							pointsEquipe5 = pointsValide
				# Ajout de la mène
				nouvelleMene = MenePartieTarot(parent = partie.key, pointsEquipe1 = pointsEquipe1, pointsEquipe2 = pointsEquipe2,  pointsEquipe3 = pointsEquipe3,  pointsEquipe4 = pointsEquipe4,  pointsEquipe5 = pointsEquipe5)
				nouvelleMene.put()
				# modification de la partie
				partie.pointsEquipe1 = partie.pointsEquipe1 + nouvelleMene.pointsEquipe1
				partie.pointsEquipe2 = partie.pointsEquipe2 + nouvelleMene.pointsEquipe2
				partie.pointsEquipe3 = partie.pointsEquipe3 + nouvelleMene.pointsEquipe3
				partie.pointsEquipe4 = partie.pointsEquipe4 + nouvelleMene.pointsEquipe4
				partie.pointsEquipe5 = partie.pointsEquipe5 + nouvelleMene.pointsEquipe5
				partie.nombreMenes = partie.nombreMenes + 1
				# Teste si la partie est terminée
				fini = False
				if partie.typePartie == 'parties':
					if partie.nombreMenes == partie.fintypeParite:
						if (partie.pointsEquipe1 > partie.pointsEquipe2) and (partie.pointsEquipe1 > partie.pointsEquipe3) and (partie.pointsEquipe1 > partie.pointsEquipe4) and (partie.pointsEquipe1 > partie.pointsEquipe5):
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe1
							fini = True
						elif (partie.pointsEquipe2 > partie.pointsEquipe1) and (partie.pointsEquipe2 > partie.pointsEquipe3) and (partie.pointsEquipe2 > partie.pointsEquipe4) and (partie.pointsEquipe2 > partie.pointsEquipe5):
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe2
							fini = True
						elif (partie.pointsEquipe3 > partie.pointsEquipe1) and (partie.pointsEquipe3 > partie.pointsEquipe2) and (partie.pointsEquipe3 > partie.pointsEquipe4) and (partie.pointsEquipe3 > partie.pointsEquipe5):
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe3
							fini = True
						elif (partie.pointsEquipe4 > partie.pointsEquipe1) and (partie.pointsEquipe4 > partie.pointsEquipe2) and (partie.pointsEquipe4 > partie.pointsEquipe3) and (partie.pointsEquipe4 > partie.pointsEquipe5):
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe4
							fini = True
						else:
							partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe5
							fini = True
				else:
					if (partie.pointsEquipe1 > partie.fintypeParite) and (partie.pointsEquipe1 > partie.pointsEquipe2) and (partie.pointsEquipe1 > partie.pointsEquipe3) and (partie.pointsEquipe1 > partie.pointsEquipe4) and (partie.pointsEquipe1 > partie.pointsEquipe5):
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe1
						fini = True
					elif (partie.pointsEquipe2 > partie.fintypeParite):
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe2
						fini = True
					elif (partie.pointsEquipe3 > partie.fintypeParite) and (partie.pointsEquipe3 > partie.pointsEquipe1) and (partie.pointsEquipe3 > partie.pointsEquipe2) and (partie.pointsEquipe3 > partie.pointsEquipe4) and (partie.pointsEquipe3 > partie.pointsEquipe5):
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe3
						fini = True
					elif (partie.pointsEquipe4 > partie.fintypeParite) and (partie.pointsEquipe4 > partie.pointsEquipe1) and (partie.pointsEquipe4 > partie.pointsEquipe2) and (partie.pointsEquipe4 > partie.pointsEquipe3) and (partie.pointsEquipe4 > partie.pointsEquipe5):
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe4
						fini = True
					elif (partie.pointsEquipe5 > partie.fintypeParite):
						partie.statusPartie = unicode('Gagnée par ', "utf-8") + partie.nomEquipe5
						fini = True
				partie.put()
			# Retourne l'ensemble des mènes de la partie
			menesEnCours = MenePartieTarot.query(ancestor=partie.key).order(MenePartieTarot.datePartie).fetch()
			return render(request, 'tarot/partieTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partie, 'menes': menesEnCours })
		else:
			# Aucune partie n'a été sélectionnée
			return render(request, 'tarot/partieTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': True, 'partie': None, 'menes': None })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def newTarot(request):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		if request.method == "POST":
			if request.POST['typePartie'] == 'parties':
				typePartie = 'parties'
				fintypeParite = request.POST['parties']
			else:
				typePartie = 'points'
				fintypeParite = request.POST['points']
			if request.POST["equipe1"] == "":
				nomEquipe1 = 'Joueur 1'
			else:
				nomEquipe1 = request.POST["equipe1"]
			if request.POST["equipe2"] == "":
				nomEquipe2 = 'Joueur 2'
			else:
				nomEquipe2 = request.POST["equipe2"]
			if request.POST["equipe3"] == "":
				nomEquipe3 = 'Joueur 3'
			else:
				nomEquipe3 = request.POST["equipe3"]
			if request.POST["equipe4"] == "":
				nomEquipe4 = 'Joueur 4'
			else:
				nomEquipe4 = request.POST["equipe4"]
			if request.POST["equipe5"] == "":
				nomEquipe5 = 'Joueur 5'
			else:
				nomEquipe5 = request.POST["equipe5"]
			# Crée la nouvelle partie
			nouvellePartie = PartieTarot(parent=ndb.Key("User", user.nickname()), statusPartie = 'En cours...', nomEquipe1 = nomEquipe1, nomEquipe2 = nomEquipe2, nomEquipe3 = nomEquipe3, nomEquipe4 = nomEquipe4, nomEquipe5 = nomEquipe5, typePartie = typePartie, fintypeParite = int(fintypeParite), nombreJoueurs = int(request.POST["joueurs"]))
			key = nouvellePartie.put()
			request.session['partieTarot'] = key.integer_id()
			# Retourne à la page de la partie en cours
			return render(request, 'tarot/partieTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': nouvellePartie, 'menes': None })
		else:
			return render(request, 'tarot/newTarot.html', { 'urlconnecte': users.create_logout_url('/') })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })

def suprimePartie(request, mene = 0):
	# Vérifie si quelqu'un est déjà connecté
	user = users.get_current_user()
	if user:
		# Retourne à la page de la partie en cours
		partieActuelle = PartieTarot.get_by_id(int(request.session.get('partieTarot')), parent=ndb.Key("User", user.nickname()))
		try:
			# Récupère la mène en cours
			meneEnCours = MenePartieTarot.get_by_id(int(mene), parent=partieActuelle.key)
			# Mise à jour de la partie
			partieActuelle.pointsEquipe1 = partieActuelle.pointsEquipe1 - meneEnCours.pointsEquipe1
			partieActuelle.pointsEquipe2 = partieActuelle.pointsEquipe2 - meneEnCours.pointsEquipe2
			partieActuelle.pointsEquipe3 = partieActuelle.pointsEquipe3 - meneEnCours.pointsEquipe3
			partieActuelle.pointsEquipe4 = partieActuelle.pointsEquipe4 - meneEnCours.pointsEquipe4
			partieActuelle.pointsEquipe5 = partieActuelle.pointsEquipe5 - meneEnCours.pointsEquipe5
			partieActuelle.nombreMenes = partieActuelle.nombreMenes - 1
			# Suppression de la mene
			meneEnCours.key.delete()
			partieActuelle.put()
		except:
			print "Erreur de suppression de la partie"
		# Récupère les mènes de la partie
		menesEnCours = MenePartieTarot.query(ancestor=partieActuelle.key).order(MenePartieTarot.datePartie).fetch()
		return render(request, 'tarot/partieTarot.html', { 'urlconnecte': users.create_logout_url('/'), 'erreur': False, 'partie': partieActuelle, 'menes': menesEnCours })
	else:
		# L'utilisateur n'est pas connecté
		return render(request, 'accueil.html', { 'urlconnecte': users.create_login_url(request.build_absolute_uri()) })
