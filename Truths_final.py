import pandas as pd #53 21 43 85
import application

import re

def detective(content,comparators):
	content_low=content.lower()
	#content_low = content_low.replace("abonnement de type season pass","")
	for a in comparators:
		a=a.lower()
		#print("is there", comparators)
		if a=="abonnement":
			if a in content_low:
				#print("is there",content_low)
				return True

		if a in content_low:
			#print("is there",content_low)
			return True
	return False


class Truth_final:
	list_apps={}
	tempoAll=[]

	def checkConsummable(self,data,count):
		check = data["Q3.8"][count]#microtransaction
		if (isinstance(check, str)):
			#checker = re.split(', | \n |,',check)
			#print(checker)
			#if(("Biens non durables (consumable)" in checker) or ("Biens non durables (<em>consumable</em>)" in checker)) or("Biens non durables " in checker)):
			# if("biens non durables" in check.lower()):
			# 	return True
			# else:
			# 	return False
			return detective(check,['Biens non durables','Monnaie','Items aléatoires'])
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
			#if(("Achat complet" in checker) or ("Retrait des publicités" in checker) or ("Biens durables (non-consumable)" in checker or("Biens non durables (<em>consumable</em>)" in checker) or ("Vente de chapitres ou de sections de jeu" in checker))):
			return detective(check,['Biens durables','Vente de chapitres ou de sections de jeu','Retrait des publicités'])
		else:
			return False

	def checkSub(self,data,count):
		check=data["Q3.8"][count]
		if (isinstance(check, str)):
			#print(detective(check,['Abonnement']),data["Q2.2_1"][count])
			checker = re.split(', | \n |,',check)
			#checker = re.split(' ', check) #TODO: fix this
			#check=check.replace("Abonnement de type Season Pass","")
			#print(check, data["Q2.2_1"][count])
			tempo=detective(check,['permettant'])
			#print(data["Q2.2_1"][count],tempo)
			#ugh=detective(check,['season'])
			#if ugh:
			#	tempo=False
			#return tempo
			return detective(check,['abonnement'])
		else:
			return False


	def checkRewarded(self,data,count):
		check=data["Q4.3"][count]
		if(isinstance(check,str)):
			checker = re.split(', | \n |,',check)
			return detective(check,['récompenses'])
		else:
			return False

	def checkInterstitial(self,data,count):
		check=data["Q4.3"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,',check)
			return detective(check, ['interstitielle'])
		else:
			return False

	def checkNative(self,data,count):
		check = data["Q4.3"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			return detective(check, ['intégrée'])
		else:
			return False

	def checkOfferwall(self,data,count):
		check = data["Q4.3"][count]
		if (isinstance(check, str)):
			#print("yes")
			checker = re.split(', | \n |,', check)
			return detective(check, ['Mur d’offres'])
		else:
			return False

	def checkInteractiveAd(self,data,count):
		check = data["Q4.3"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			return detective(check, ['interactive'])
		else:
			return False

	def checkNotification(self,data,count):
		check = data["Q5.2"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			return detective(check, ['notifications'])
		else:
			return False

	def checkNotifPerm(self,data,count):
		check = data["Q6.15"][count]
		if (isinstance(check, str)):
			checker = re.split(', | \n |,', check)
			return detective(check, ['notifications'])
		else:
			return False


	def checkLeaderboard(self,data,count):
		check = data["Q5.5"][count]
		#TODO:find what is the real error return
		if(isinstance(check,str)):
			checker = re.split(', | \n |,', check)
			return detective(check, ['classement'])
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
			return detective(check, ['Retrait des publicités'])
		else:
			return False

	def get_indicated_id(self,data,count):
		tempo_more = data["Q2.3.1"][count]
		is_nan_more = (isinstance(tempo_more, str))
		if is_nan_more:
			url = data["Q2.3.1"][count].strip()
			pos = url.find("id")
			url = url[(pos + 3):]
			end = url.find("&")
			if (not end == -1):
				url = url[:end]
				return url
			else:
				return ""
		else:
			return ""

	def time_converter(self,date):
		if(len(date)>10):
			#print(date)
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

	# def get_indicated_id(self,data,count):
	# 	url = data["Q2.3.1"][count].strip()
	# 	pos = url.find("id")
	# 	url = url[(pos + 3):]
	# 	end = url.find("&")
	# 	if (not end == -1):
	# 		indicated_id = url[:end]
	# 		return indicated_id
	# 	else:
	# 		return ""


	def loadTruth_final(self,file):
		print(file,"final")
		#TODO:remove hard-coded value
		#data = pd.read_excel(r"Donnees_vraies.xlsx")
		#data = pd.read_excel(io=file,sheet_name="Données (total)")
		data = pd.read_excel(io=file, sheet_name="Données (total)")
		secondata=pd.read_excel(io=file,sheet_name="Sheet1")
		seconddf=pd.DataFrame(secondata)
		#df=pd.DataFrame(data,columns=["Titre du jeu (Android)"])
		df=pd.DataFrame(data)
		for count in range(len(df["Q2.2_1"])): #Titre de jeu (Android)
			#try:
			app=application.application()
			tempo = df["Q2.2_1"][count]
			tempo2 = df["Q4.2"][count]
			tempo3 = df["Q3.2"][count]
			# print(tempo3=="Gratuit")
			is_nan = (isinstance(tempo, str) and (isinstance(tempo2, str) or isinstance(tempo2, bool) or True) and isinstance(tempo3, str))
			if is_nan:
				if tempo3.lower()=="gratuit":
					app.gratuite=True
				if tempo3.lower()=="payant":
					app.gratuite=True
			#tempo_more = seconddf["Q2.3.1"][count]
			tempo_more = df["Q2.2_1"][count]
			is_nan_more = (isinstance(tempo_more, str))
			if is_nan and app.gratuite:
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
				#print(app.subIAP,"######",app.name,count)
				#print("###########",self.checkSub(seconddf,count),"########",app.name,count)
				#print(app.subIAP,app.name)
				app.offerwall=self.checkOfferwall(df,count)

				app.rewardedAds=self.checkRewarded(df,count)
				app.interstitialAds=self.checkInterstitial(df,count)
				app.interactiveAds=self.checkInteractiveAd(df,count)
				app.nativeAds=self.checkNative(df,count)

				app.push_notification=self.checkNotification(df,count)

				app.leaderboard=self.checkLeaderboard(df,count)
				app.shownDeveloper=self.checkDeveloper(df,count)
				app.removeAds=self.checkRemoveAds(df,count)

				app.indicated_id=self.get_indicated_id(df,count)

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
		#print("aaaaaaa######################################")
		# for count in range(len(seconddf["Q2.2_1"])):
		# 	#print("aaaabeforea", app.name, app.subIAP, count)
		# 	tempo = seconddf["Q2.2_1"][count]
		# 	tempo2 = df["Q4.2"][count]
		# 	tempo3 = df["Q3.2"][count]
		# 	# print(tempo3=="Gratuit")
		# 	is_nan = (isinstance(tempo, str) and (isinstance(tempo2, str) or isinstance(tempo2, bool)) and tempo3 == "Gratuit")
		# 	if is_nan:
		# 	#if False:
		# 		if(not (tempo in self.list_apps)):
		# 			app = application.application()
		# 		else:
		# 			app = self.list_apps[tempo]
		# 			#print(app.name)
		# 		app.name=df["Q2.2_1"][count].strip()
		# 		#print(app.name,df["Q3.8"][count])
		# 		app.subIAP = self.checkSub(seconddf, count) | app.subIAP
		# 		#print("beforea", app.name, app.subIAP,count)
		# 		if (not app.name in self.list_apps):
		# 			self.list_apps[app.name] = app


	def getTruths_final(self):
		return self.list_apps