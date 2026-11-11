import pandas as pd
import application

import re

class Truth:
	list_apps={}

	def checkConsummable(self,data,count):
		check=data["Détails des microtransactions observées"][count]
		checker = re.split(', | \n |,',check)
		if("Consumable" in checker):
			return True
		else:
			return False

	def getYearPub(self,data,count):
		check=data["Année de publication"][count]
		return check.strip()

	def checkPermanent(self,data,count):
		check = data["Détails des microtransactions observées"][count]
		#checker = check.split(",")
		checker = re.split(', | \n |,',check)
		if(("Non-consumable" in checker) or ("Retrait des publicités" in checker) or("Vente du jeu complet" in checker)):
			return True
		else:
			return False

	def checkSub(self,data,count):
		check=data["Détails des microtransactions observées"][count]
		checker = re.split(', | \n |,',check)
		if("Abonnement" in checker):
			return True
		else:
			return False


	def checkRewarded(self,data,count):
		check=data["Types de publicités "][count]
		checker = re.split(', | \n |,',check)
		if("Publicité rewarded Video Ads" in checker):
			return True
		else:
			return False

	def checkInterstitial(self,data,count):
		check=data["Types de publicités "][count]
		checker = re.split(', | \n |,',check)
		if("Publicité interstitielle" in checker):
			return True
		else:
			return False

	def checkNative(self,data,count):
		check = data["Types de publicités "][count]
		checker = re.split(', | \n |,', check)
		if ("Publicité intégrée" in checker):
			return True
		else:
			return False

	def checkOfferwall(self,data,count):
		check = data["Types de publicités "][count]
		checker = re.split(', | \n |,', check)
		if ("Publicité intégrée" in checker):
			return True
		else:
			return False

	def checkInteractiveAd(self,data,count):
		check = data["Types de publicités "][count]
		checker = re.split(', | \n |,', check)
		if ("Publicité interactive" in checker):
			return True
		else:
			return False

	def checkNotification(self,data,count):
		check = data["Mécaniques associées à la structure du jeu"][count]
		try:
			checker = re.split(', | \n |,', check)
		except:
			return False
		if ("Notifications poussées" in checker):
			return True
		else:
			return False

	def checkLeaderboard(self,data,count):
		check = data["Mécaniques associées à la sociabilité"][count]
		#TODO:find what is the real error return
		try:
			checker = re.split(', | \n |,', check)
		except:
			return False
		if ("Tableaux de classement" in checker):
			return True
		else:
			return False

	def checkDeveloper(self,data,count):
		#print(data["Développeur"][count])
		check=data["Développeur"][count]
		return check



	def loadTruth(self,file):
		#TODO:remove hard-coded value
		#data = pd.read_excel(r"Donnees_vraies.xlsx")
		data = pd.read_excel(file)
		#df=pd.DataFrame(data,columns=["Titre du jeu (Android)"])
		df=pd.DataFrame(data)
		for count in range(len(df["Titre du jeu (Android)"])):

			#print("inside",df["Titre du jeu (Android)"][count].strip())
			app=application.application()
			app.name=df["Titre du jeu (Android)"][count].strip()
			app.publicationYear=df["Année de publication"][count]
			app.version=df["Version testée"][count]

			app.consummableIAP = self.checkConsummable(df, count)
			app.permanentIAP = self.checkPermanent(df,count)
			app.subIAP = self.checkSub(df,count)

			app.rewardedAds=self.checkRewarded(df,count)
			app.interstitialAds=self.checkInterstitial(df,count)
			app.interactiveAds=self.checkInteractiveAd(df,count)
			app.nativeAds=self.checkNative(df,count)

			app.push_notification=self.checkNotification(df,count)

			app.leaderboard=self.checkLeaderboard(df,count)
			app.shownDeveloper=self.checkDeveloper(df,count)

			#print(app.name,app.nativeAds)

			self.list_apps[app.name]=app


	def getTruths(self):
		return self.list_apps


