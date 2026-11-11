import Model
import Truths
from Model import loadTranslation
from application import application

list_applis = []

list_Truths = {}

reals = Truths.Truth()
reals.loadTruth("Donnees_vraies.xlsx")
list_Truths = reals.getTruths()

translation = loadTranslation()

def separate(one,two):
	print("yay")