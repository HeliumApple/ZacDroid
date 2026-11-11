import google_play_scraper
from google_play_scraper import app

import Truths
from Model import loadTranslation
from Truths import Truth


def getStoreName(id):
	try:
		infos = app(id)#, country='ca')
		#print(application.id)
	except:
		print("couldn't find",id)
		return None
	if (infos["title"] is not None):
		Title = infos["title"]
		return Title
	else:
		return None


def getOnlyID(line):
	appInfo=line.split("\\")
	idStart=appInfo[1].find("[")+1
	idEnd=appInfo[1].find("]")
	Id=appInfo[1][idStart:idEnd]
	ugh=[appInfo[0],Id]
	if(not(Id=="")):
		return ugh
	else:
		#print(appInfo)
		return ["",""]

f = open("appInfo/AppId_Final.txt",encoding="utf8")


translation=loadTranslation()

list_Truths = {}

reals = Truths.Truth()
reals.loadTruth("Donnees_vraies.xlsx")
list_Truths = reals.getTruths()

d = open("appid_version","a")

for a in f:
	info=getOnlyID(a)
	if(info[0] in list_Truths):
		res=list_Truths[info[0]]
		#print(str(res.version)+"\n")
		#print(info[1]+","+str(res.version)+"\n")
		d.write(info[1]+","+str(res.version)+"\n")
		#print(res.name,res.version)