#-*- coding: utf-8 -*-
from django.shortcuts import render
# Imports de App Engine
from google.appengine.api import users

def accueil(request):
	# Page d'aide et de présentation de l'outil
	user = users.get_current_user()
	return render(request, 'accueil.html', { 'urlconnecte': users.create_logout_url('/') })

def regles(request):
	# Affiche les références des règles officielles
	user = users.get_current_user()
	return render(request, 'informations/regles.html', { 'urlconnecte': users.create_logout_url('/') })

def configuration(request):
	# Retourne la page donnant les informations sur les version en cours
	user = users.get_current_user()
	return render(request, 'informations/configuration.html', { 'urlconnecte': users.create_logout_url('/') })
