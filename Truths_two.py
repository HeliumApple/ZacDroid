import pandas as pd
import application

import re

class Truth_two:
	list_apps={}
	tempoAll=[]

	def checkConsummable(self,data,count):
		check = data["Q3.8"][count]#microtransaction
		if (isinstance(check, str)):
			checker = re.split(', | \n |,',check)
			#print(checker)
			if(("Biens non durables (consumable)" in checker) or ("Biens non durables (<em>consumable</em>)" in checker)):
				return True
			else:
				return False
		else:
			return False

	def getYearPub(self,data,count):
		check=data["Q2.5_5"][count]
		return check.strip()

	def checkPermanent(self,data,count):
		check = data["Q3.8"][count]
		if (isinstance(check, str)):
		#checker = check.split(",")
			#check = "Biens non durables (consumable),Monnaie « Premium » (conversion de devises/hard currency)"
			checker = re.split(', | \n |,',check)
			#print(checker)
			if(("Achat complet" in checker) or ("Retrait des publicités" in checker) or ("Biens durables (non-consumable)" in checker or("Biens non durables (<em>consumable</em>)" in checker) or ("Vente de chapitres ou de sections de jeu" in checker))):
				return True
			else:
				return False
		else:
			return False

	def checkSub(self,data,count):
		check=data["Q3.8"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,',check)
			#checker = re.split(' ', check) #TODO: fix this
			if(("Abonnement" in checker) or("Abonnement permettant l'accès au jeu et/ou du contenu jouable supplémentaire" in checker) or ("Abonnement de type Season Pass (peut inclure biens durables et non durables)" in checker)):
				return True
			else:
				return False
		else:
			return False


	def checkRewarded(self,data,count):
		check=data["Q4.3"][count]
		if(isinstance(check,str)):
			checker = re.split(', | \n |,',check)
			if("Annonce avec récompenses (rewarded ads)" in checker or "Annonce avec récompenses (<em>rewarded ads</em>)" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkInterstitial(self,data,count):
		check=data["Q4.3"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,',check)
			if("Publicité interstitielle" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkNative(self,data,count):
		check = data["Q4.3"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			if ("Publicité intégrée" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkOfferwall(self,data,count):
		check = data["Q4.3"][count]
		if (isinstance(check, str)):
			#print("yes")
			checker = re.split(', | \n |,', check)
			if ("Mur d’offres (offerwall)" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkInteractiveAd(self,data,count):
		check = data["Q4.3"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			if ("Publicité interactive" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkNotification(self,data,count):
		check = data["Q5.2"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			if ("Notifications poussées" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkLeaderboard(self,data,count):
		check = data["Q5.5"][count]
		#TODO:find what is the real error return
		if(isinstance(check,str)):
			checker = re.split(', | \n |,', check)
			if ("Tableaux de classement" in checker):
				return True
			else:
				return False
		else:
			return False

	def checkDeveloper(self,data,count):
		#print(data["Développeur"][count])
		check=data["Q2.5_4"][count]
		return check

	def checkRemoveAds(self,data,count):
		check = data["Q3.8"][count]
		# TODO:find what is the real error return
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			if ("Retrait des publicités" in checker):
				return True
			else:
				return False
		else:
			return False

	def time_converter(self,date):
		if(len(date)>10):
			print(date)
			tempo=date.split(' ')
			days=tempo[0]
			time=tempo[1]

			tempo2=days.split('-')
			month=tempo2[0]
			day=tempo2[1]
			year=tempo2[2]

			if(month<10):
				month="0"+month
			if(day<10):
				day="0"+day

			newDate=year+"-"+month+"-"+day
			return newDate
		else:
			return 'zzzzzz'



	def loadTruth_two(self,file):
		#TODO:remove hard-coded value
		#data = pd.read_excel(r"Donnees_vraies.xlsx")
		data = pd.read_excel(file)
		#df=pd.DataFrame(data,columns=["Titre du jeu (Android)"])
		df=pd.DataFrame(data)
		for count in range(len(df["Q2.2_1"])): #Titre de jeu (Android)
			#try:
			app=application.application()
			#print(df["Q2.2_1"][count])
			tempo=df["Q2.2_1"][count]
			tempo2=df["Q4.2"][count]
			#tempo_more=df["Q2.3.1"][count]
			#is_nan = pd.isna(df["Q2.2_1"][count])
			is_nan=(isinstance(tempo,str) and isinstance(tempo2,str))
			is_nan=(isinstance(tempo,str))
			#is_nan_more=(isinstance(tempo_more,str))
			#print(df["Q4.2"][count])
			if is_nan:
				#print("inside",df["Q2.2_1"][count].strip())
				app.name=df["Q2.2_1"][count].strip()
				#testDate=df["StartDate"][count]#.strip()
				#app.dateTest = str(testDate)
				app.publicationYear=df["Q2.5_5"][count]#année publication
				app.publicationYear=count
				app.version=df["Q2.8_1"][count]#version testé

				app.consummableIAP = self.checkConsummable(df, count)
				app.permanentIAP = self.checkPermanent(df,count)
				app.subIAP = self.checkSub(df,count)
				app.offerwall=self.checkOfferwall(df,count)

				app.rewardedAds=self.checkRewarded(df,count)
				app.interstitialAds=self.checkInterstitial(df,count)
				app.interactiveAds=self.checkInteractiveAd(df,count)
				app.nativeAds=self.checkNative(df,count)

				app.push_notification=self.checkNotification(df,count)

				app.leaderboard=self.checkLeaderboard(df,count)
				app.shownDeveloper=self.checkDeveloper(df,count)
				app.removeAds=self.checkRemoveAds(df,count)

				#if is_nan_more:
				#	app.url=df["Q2.3.1"][count].strip()

			#print(app.name,app.nativeAds)
				#print(app.name)

				# if(app.name in self.list_apps):
				# 	print("what?")
				# 	#print(app.name)
				# 	if(app.dateTest>self.list_apps[app.name].dateTest):
				#
				# 		print(app.dateTest,"is better than",self.list_apps[app.name].dateTest)
				# 		self.list_apps[app.name].recent=False
				# 		app.recent=True
				# 		self.list_apps[app.name]=app
				# 	else:
				# 		print(app.dateTest, "is not better than", self.list_apps[app.name].dateTest)
				# 		#app.name = app.name + " "+app.dateTest
				# 		app.recent=False
				# else:
				# 	self.list_apps[app.name] = app
				self.list_apps[app.name] = app
			#except:
			else:
				a=0
				#print("nope :(")
		print("######################################")



	def getTruths_two(self):
		return self.list_apps