#-*- coding: utf-8 -*-
from google.appengine.ext import ndb

# Gestion d'une partie
class PartieTarot(ndb.Model):
	statusPartie = ndb.StringProperty()
	nomEquipe1 = ndb.StringProperty(default = 'Joueur 1')
	nomEquipe2 = ndb.StringProperty(default = 'Joueur 2')
	nomEquipe3 = ndb.StringProperty(default = 'Joueur 3')
	nomEquipe4 = ndb.StringProperty(default = 'Joueur 4')
	nomEquipe5 = ndb.StringProperty(default = 'Joueur 5')
	nombreJoueurs = ndb.IntegerProperty(default = 3)
	nombreMenes = ndb.IntegerProperty(default = 0)
	pointsEquipe1 = ndb.IntegerProperty(default = 0)
	pointsEquipe2 = ndb.IntegerProperty(default = 0)
	pointsEquipe3 = ndb.IntegerProperty(default = 0)
	pointsEquipe4 = ndb.IntegerProperty(default = 0)
	pointsEquipe5 = ndb.IntegerProperty(default = 0)
	datePartie = ndb.DateTimeProperty(auto_now_add=True)
	typePartie = ndb.StringProperty()	
	fintypeParite = ndb.IntegerProperty(default = 10)

# Gestion des mènes d'une partie
class MenePartieTarot(ndb.Model):
	typeMene = ndb.StringProperty()
	pointsEquipe1 = ndb.IntegerProperty(default = 0)
	pointsEquipe2 = ndb.IntegerProperty(default = 0)
	pointsEquipe3 = ndb.IntegerProperty(default = 0)
	pointsEquipe4 = ndb.IntegerProperty(default = 0)
	pointsEquipe5 = ndb.IntegerProperty(default = 0)
	datePartie = ndb.DateTimeProperty(auto_now_add=True)
