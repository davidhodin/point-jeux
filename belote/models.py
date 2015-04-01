#-*- coding: utf-8 -*-
from google.appengine.ext import ndb

# Gestion des mènes d'une partie
class MenePartieBelotte(ndb.Model):
	pointsEquipe1 = ndb.IntegerProperty(default = 0)
	pointsEquipe2 = ndb.IntegerProperty(default = 0)
	beloteEquipe1 = ndb.BooleanProperty(default = False)
	beloteEquipe2 = ndb.BooleanProperty(default = False)
	datePartie = ndb.DateTimeProperty(auto_now_add=True)

# Gestion d'une partie
class PartieBelotte(ndb.Model):
	statusPartie = ndb.StringProperty()
	nomEquipe1 = ndb.StringProperty(default = 'Equipe 1')
	nomEquipe2 = ndb.StringProperty(default = 'Equipe 2')
	nombreMenes = ndb.IntegerProperty(default = 0)
	pointsEquipe1 = ndb.IntegerProperty(default = 0)
	pointsEquipe2 = ndb.IntegerProperty(default = 0)
	datePartie = ndb.DateTimeProperty(auto_now_add=True)
	typePartie = ndb.StringProperty()
	fintypeParite = ndb.IntegerProperty(default = 10)
	litigeDernierePartie = ndb.IntegerProperty(default = 0)

