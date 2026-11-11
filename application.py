class application:
	def __init__(self):

		self.UseUnity=False
		self.NotifPerm=False

		self.Title=""
		self.exist=False
		self.gratuite=True

		self.shownDeveloper=""
		self.developer = ""
		self.developerCountry = ""
		self.publicationYear = ""
		self.Downloads = ""
		self.Note = ""
		self.category = ""
		self.ESRB = ""
		self.TeacherApproved = ""
		self.iap_minPrice = 0
		self.iap_maxPrice = 0

		self.PrivacyPolicy = False

		self.id = ""
		self.name = ""
		self.consummableIAP = False##
		self.permanentIAP = False##
		self.subIAP = False

		self.rewardedAds = False
		self.interstitialAds = False
		self.offerwall = False
		self.nativeAds = False
		self.interactiveAds = False

		self.push_notification = False
		self.pushFCM=False

		self.leaderboard = False

		self.removeAds = False

		self.dateTest = "00-00-0000"
		self.recent=True

		self.version=0

		self.url=""
		self.indicated_id=""
		self.test1=False
		self.test2=False
		self.test3=False
		self.test4=False
		self.test5=False
		self.test6=False
		self.test7=False
		self.test8=False

		self.test9=False
		self.test10=False
		self.test11=False
		self.test12=False
		self.test13=False
		self.test14=False
		self.test15=False
		self.test16=False

		self.test17=False
		self.test18=False
		self.test19=False
		self.test20=False
		self.test21=False
		self.test22=False
		self.test23=False
		self.test24=False

		#TrueN,TrueP,FalseN,FalseP
		self.CompIAP=[0,0,0,0]
		self.CompAds=[0,0,0,0]
		self.CompStructure=[0,0,0,0]
		self.CompSocial=[0,0,0,0]
		self.CompTest=[0,0,0,0]

	def showResult(self):
		#print(self.name + " may have the following:")
		if (self.consummableIAP):
			print("Consummable microtransaction")
		if (self.permanentIAP):
			print("non-consummable microtransaction")
		if (self.subIAP):
			print("subscriptions")

	def getData(self):
		data = {
			"general":[self.Title,self.developer,self.publicationYear,self.Downloads,self.Note,self.category,self.ESRB,self.PrivacyPolicy,self.version],
			"ads":[self.Title,self.rewardedAds,self.interstitialAds,self.nativeAds,self.offerwall],
			"IAP":[self.Title,self.consummableIAP,self.permanentIAP,self.subIAP,self.removeAds],
			"social":[self.Title,self.leaderboard],
			"structure":[self.Title,self.push_notification],
			"test":[self.Title,self.test1,self.test2,self.test3,self.test4,self.test5,self.test6,self.test7,self.test8],
			"test2": [self.Title, self.test9, self.test10, self.test11, self.test12, self.test13, self.test14, self.test15,
			         self.test16],
			"test3": [self.Title, self.test17, self.test18, self.test19, self.test20, self.test21, self.test22, self.test23,
			         self.test24]
		}

		return data

	def getComparision(self,otherApp):
		DataSelf=self.getData()
		DataOther=otherApp.getData()

		adsSelf=DataSelf["ads"]
		adsOther=DataOther["ads"]

		IAPSelf=DataSelf["IAP"]
		IAPOther=DataOther["IAP"]

		SocialSelf=DataSelf["social"]
		SocialOther=DataOther["social"]

		StructureSelf=DataSelf["structure"]
		StructureOther=DataOther["structure"]

		TestSelf=DataSelf["test"]
		#TestOther=DataOther["test"]
		#TestOther=bool(DataOther["structure"][1])
		TestOther = bool(DataOther["ads"][2])# | bool(DataOther["IAP"][1])

		test2Self=DataSelf["test2"]
		Test2Other=bool(DataOther["ads"][1])# | bool(DataOther["IAP"][1])

		test3Self=DataSelf["test3"]
		Test3Other = bool(DataOther["structure"][1])# | bool(DataOther["IAP"][1])


		comparison={
			#"ads":[not (bool(self.rewardedAds)^bool(otherApp.rewardedAds)),not (bool(self.interstitialAds)^bool(otherApp.interstitialAds)),not (bool(self.offerwall)^bool(otherApp.offerwall))],
			"ads": [not (bool(adsSelf[1]) ^ bool(adsOther[1])),not (bool(adsSelf[2]) ^ bool(adsOther[2])),not (bool(adsSelf[3]) ^ bool(adsOther[3])), not (bool(adsSelf[4]) ^ bool(adsOther[4]))],
			#"IAP":[not (bool(self.consummableIAP)^bool(otherApp.consummableIAP)),not (bool(self.permanentIAP)^bool(otherApp.permanentIAP)),not (bool(self.subIAP)^bool(otherApp.subIAP))],
			"IAP":[not bool(IAPSelf[1] ^ bool(IAPOther[1])), not (bool(IAPSelf[2]) ^ bool(IAPOther[2])),not (bool(IAPSelf[3]) ^ bool(IAPOther[3])),not (bool(IAPSelf[4]) ^ bool(IAPOther[4]))],
			#"social":[not (bool(self.leaderboard)^bool(otherApp.leaderboard))],
			"social":[not (bool(SocialSelf[1] ^ bool(SocialOther[1])))],
			#"structure":[not (bool(self.push_notification^bool(otherApp.push_notification)))]
			"structure":[not (bool(StructureSelf[1]) ^ bool(StructureOther[1]))],
			#"test": [not (bool(TestSelf[1]) ^ bool(TestOther[1])),not (bool(TestSelf[2]) ^ bool(TestOther[2])),not (bool(TestSelf[3]) ^ bool(TestOther[3])), not (bool(TestSelf[4]) ^ bool(TestOther[4])),not (bool(TestSelf[5]) ^ bool(TestOther[5])),not (bool(TestSelf[6]) ^ bool(TestOther[6]))]
			"test": [not (bool(TestSelf[1]) ^ TestOther), not (bool(TestSelf[2]) ^ TestOther),
			         not (bool(TestSelf[3]) ^ TestOther), not (bool(TestSelf[4]) ^ TestOther),
			         not (bool(TestSelf[5]) ^ TestOther), not (bool(TestSelf[6]) ^ TestOther),
			         not (bool(TestSelf[7]) ^ TestOther), not (bool(TestSelf[8]) ^ TestOther)],

			"test2": [not (bool(test2Self[1]) ^ Test2Other), not (bool(test2Self[2]) ^ Test2Other),
			         not (bool(test2Self[3]) ^ Test2Other), not (bool(test2Self[4]) ^ Test2Other),
			         not (bool(test2Self[5]) ^ Test2Other), not (bool(test2Self[6]) ^ Test2Other),
			         not (bool(test2Self[7]) ^ Test2Other), not (bool(test2Self[8]) ^ Test2Other)],

			"test3": [not (bool(test3Self[1]) ^ Test3Other), not (bool(test3Self[2]) ^ Test3Other),
			         not (bool(test3Self[3]) ^ Test3Other), not (bool(test3Self[4]) ^ Test3Other),
			         not (bool(test3Self[5]) ^ Test3Other), not (bool(test3Self[6]) ^ Test3Other),
			         not (bool(test3Self[7]) ^ Test3Other), not (bool(test3Self[8]) ^ Test3Other)]
		}

		return comparison


	def getIAPStat(self,otherApp):
		DataSelf=self.getData()
		DataOther=otherApp.getData()
		adsSelf=DataSelf["IAP"]
		adsOther=DataOther["IAP"]
		#IAP
		comparison=[not (bool(adsSelf[1]) ^ bool(adsOther[1])),not (bool(adsSelf[2]) ^ bool(adsOther[2])),not (bool(adsSelf[3]) ^ bool(adsOther[3]))]
		for count in range(len(comparison)):
			#if(comparison["ads"]):
			if(comparison[count]):
				#true result
				if(adsSelf[0]):
					self.CompIAP[1]+=1
				else:
					self.CompIAP[0]+=1
			else:
				#false result
				if(adsSelf[0]):
					self.CompIAP[3]+=1
				else:
					self.CompIAP[2]+=1
		return self.CompIAP

	def getAdsStat(self,otherApp):
		DataSelf=self.getData()
		DataOther=otherApp.getData()
		adsSelf=DataSelf["ads"]
		adsOther=DataOther["ads"]
		#IAP
		comparison=[not (bool(adsSelf[1]) ^ bool(adsOther[1])),not (bool(adsSelf[2]) ^ bool(adsOther[2])),not (bool(adsSelf[3]) ^ bool(adsOther[3])),not (bool(adsSelf[4]) ^ bool(adsOther[4])) ]
		for count in range(len(comparison)):
			#if(comparison["ads"]):
			if(comparison[count]):
				#true result
				if(adsSelf[0]):
					self.CompAds[1]+=1
				else:
					self.CompAds[0]+=1
			else:
				#false result
				if(adsSelf[0]):
					self.CompAds[3]+=1
				else:
					self.CompAds[2]+=1
		return self.CompAds

	def getSocialStat(self,otherApp):
		DataSelf=self.getData()
		DataOther=otherApp.getData()
		adsSelf=DataSelf["social"]
		adsOther=DataOther["social"]
		#IAP
		comparison=[not (bool(adsSelf[1]) ^ bool(adsOther[1]))]#,not (bool(adsSelf[2]) ^ bool(adsOther[2])),not (bool(adsSelf[3]) ^ bool(adsOther[3]))]
		for count in range(len(comparison)):
			#if(comparison["ads"]):
			if(comparison[count]):
				#true result
				if(adsSelf[0]):
					self.CompSocial[1]+=1
				else:
					self.CompSocial[0]+=1
			else:
				#false result
				if(adsSelf[0]):
					self.CompSocial[3]+=1
				else:
					self.CompSocial[2]+=1
		return self.CompSocial

	def getStructureStat(self,otherApp):
		DataSelf=self.getData()
		DataOther=otherApp.getData()
		adsSelf=DataSelf["structure"]
		adsOther=DataOther["structure"]
		#IAP
		comparison=[not (bool(adsSelf[1]) ^ bool(adsOther[1]))]#,not (bool(adsSelf[2]) ^ bool(adsOther[2])),not (bool(adsSelf[3]) ^ bool(adsOther[3]))]
		for count in range(len(comparison)):
			#if(comparison["ads"]):
			if(comparison[count]):
				#true result
				if(adsSelf[0]):
					self.CompStructure[1]+=1
				else:
					self.CompStructure[0]+=1
			else:
				#false result
				if(adsSelf[0]):
					self.CompStructure[3]+=1
				else:
					self.CompStructure[2]+=1
		return self.CompStructure

	def getTestStat(self,otherApp):
		DataSelf=self.getData()
		DataOther=otherApp.getData()
		TestSelf=DataSelf["test"]
		TestOther=DataOther["test"]
		comparison=[not bool(TestSelf[1] ^ bool(TestOther[1])),not bool(TestSelf[2] ^ bool(TestOther[2])),not bool(TestSelf[3] ^ bool(TestOther[3])),not bool(TestSelf[4] ^ bool(TestOther[4])),not bool(TestSelf[5] ^ bool(TestOther[5])),not bool(TestSelf[6] ^ bool(TestOther[6]))]
		for count in range(len(comparison)):
			if(comparison[count]):
				if(TestSelf[0]):
					self.CompTest[1]+=1
				else:
					self.CompTest[0]+=1
			else:
				if(TestSelf[0]):
					self.CompTest[3]+=1
				else:
					self.CompTest[2]+=1
		return self.CompTest