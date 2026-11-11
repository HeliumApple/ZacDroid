import concurrent.futures
import json
import os
import re
import time
from collections import defaultdict
from contextlib import contextmanager
import loguru

from google_play_scraper import app

import Truths_final
import Truths_two
import application

from concurrent.futures import as_completed

"""contiens les IDs des applications avec le nom correspondant"""
#translation_file="translation_file.txt"
#mode=""


def strToBool(string):
	"""convert string value to boolean type
	 ARGS: string value(must be "true" or "false", case insensitive)
	 return boolean value
	 """
	if(string.lower()=="true"):
		return True
	else:
		return False

def loadTranslation(filename,mode):
	"""
	load translation file
	:param filename: path of the file used for translation
		file format: one application per line, formatted as :
			id,name
	:param mode: 0 or 1
	:return: dictionary which key depend on the mode
	mode 0: key is the application's id and value is the application's name
	mode 1: key is the application's name and value is the application's id
	"""
	Names={}
	with open(filename,encoding="utf-8") as file:
		for line in file:
			tempo=line.split(",")
			key=tempo.pop(0)
			val = ",".join(tempo)
			key=key.strip()
			val=val.strip()
			if mode==0:
				Names[key]=val
			elif mode==1:
				Names[val]=key
	return Names


def GetStoreInfo(application):
	"""
		get some informations present on the Google play Store
		Arg:
			application: application objet with an id value
		return:
			same application objet with relevant values
	"""
	try:
		infos = app(application.id)
		#print(application.id)
	except:
		print("(getstoreinfo)couldn't find",application.id)
		#TODO: make this safer
		application.Title=application.id
		return 0
	if(infos["developer"] is not None):
		application.developer = infos["developer"]
	if(infos["released"] is not None):
		application.publicationYear = infos["released"][-4:]
	else:
		application.publicationYear = -1

	if(infos["realInstalls"] is not None):
		application.Downloads = str(infos["realInstalls"])

	if(infos["score"] is not None):
		application.Note = str(infos["score"])

	if(infos["genre"] is not None):
		application.category = infos["genre"]

	if(infos["contentRating"] is not None):
		application.ESRB = infos["contentRating"]

	if(infos["title"] is not None):
		application.Title=infos["title"]
	prices = infos["inAppProductPrice"]
	if(prices is not None):
		prices = prices.split()
		minprice=prices[0][1:]
		while "," in minprice: minprice.remove(",")
		application.iap_minPrice=float(minprice)
		if (len(prices) > 3):
			maxprice=prices[2][1:]
			maxprice=maxprice.replace(",","")
			application.iap_maxPrice = float(maxprice)
		else:
			application.iap_maxPrice = application.iap_minPrice
	privacy_policy = infos["privacyPolicy"]
	if(privacy_policy is not None):
		if (len(privacy_policy) > 0):
			application.PrivacyPolicy = True
	return 1

def getContext(i,fileLines):
	"""
	get the context around a given line of a file
	:param i: the index of the concerned line
	:param fileLines: list containing the lines of a file
	:return: a string of the lines before and after the concerned line
	"""
	width=10
	con=""
	if i>width and i<(len(fileLines)-width):
		for l in range(i-width,i+width):
			con=con+fileLines[l]

	return con


file_count=0
file_done=0
threshold=0

jadx = True

@contextmanager
def loguru_disable(name):
	# TODO: check if necessary with modified androguard library and add documentation
	# disable some logging stuff
    loguru.logger.disable(name)
    try:
        yield
    finally:
        loguru.logger.enable(name)


# @loguru_disable("androguard")
# def test(name):
# 	q, w, es = AnalyzeAPK(name)
# 	return q, w, es

#(change if required) interstitial ads

#format for this one: precision/recall, shown below the pattern
# test1="onInterstitialDisplayed" #Facebook audience network
# #1.0/0.099
# test2="InterstitialAd.load" #google
# #0.71/1.0
# test3="ShowInterstitialAd" #unity(ish? from google?)
# #0.868/0.831
# test4="MaxInterstitialAd" #applovin
# #0.922/0.831
# test5="showInterstitial" #ironsource
# #0.676/1.0
# test6="import com.vungle.ads.InterstitialAd" #vungle
# #0.808/0.296
# test7="getmaxadcount"
# #0.921/0.817
# test8="getmaxpreloadedadcount"
# #0.921/0.817

sku_pattern = re.compile(r'["\']([\w\d._-]+)["\']')  # matches strings
subs_type_pattern_sku = re.compile(r'BillingClient\.SkuType\.SUBS|"subs"')
inapp_type_pattern_sku = re.compile(r'BillingClient\.SkuType\.INAPP|"inapp"')
consume_pattern_sku = re.compile(r'consumeAsync\s*\(')
persist_pattern_sku = re.compile(r'putBoolean|putString|save|prefs\.edit\(\)')

# test1="loadbanneradasync"
# test2="setadsize(adsize.banner)"
# test3="setadsize(adsize\.banner)"
# test4="bannerview"
# test5="MaxAdView"
# test6="BannerAdView"
# test7="adconfig.adsize.banner"
# test8="adconfig\.adsize\.banner"

# test1="onUserEarnedReward" #google
# test2="RewardedVideoAdListener" #facebook thing
# test3="DisplayRewardedVideoAd" #unity
# test4="createRewardedAd" #lovin app thing
# test5="showRewardedAd" #ironsource
# test6="new RewardedAd" #vungle
# test7="new PAGRewardedRequest" #pangle
# test8="RewardedAd.load()" #Mintegral mbbanner?

# test9="OnInterstitialDisplayed"
# test10="InterstitialAd.load"
# test11="ShowInterstitialAd"
# test12="MaxInterstitialAd"
# test13="showInterstitial"
# test14="Import com.vungle.ads.interstitialAd"
# test15="getmaxadcount"
# test16="getmaxpreloadedadcount"

# test9="loadbanneradasync"
# test10="setadsize(adsize.banner)"
# test11="size=\"banner\""
# test12="size=\'banner\'"
# test13="size=\'BANNER\'"
# test14="size=\"BANNER\""
# test15="size"
# test16="banner"


# test9="pagbanneradloadlistener"
# test10="banner.loadAd"
# test11="banner\.loadAd"
# test12="com.google.android.gms.gcm.GcmReceiver"
# test13="android.app.NotificationManager"
# test14="com.google.firebase.MESSAGING_EVENT"
# test15="com.google.android.c2dm.intent.RECEIVE"
# test16="com.google.firebase.INSTANCE_ID_EVENT"
#(change if required) interstitial ads
# test9="permanentpurchase"
# test10="permanent_purchase"
# test11=" permanentpurchase"
# test12=" permanent_purchase"
# test13="unlock_purchase"
# test14="unlockpurchase"
# test15=" unlock_purchase"
# test16=" unlockpurchase"


# test1="NotificationCompat.Builder"
# test2="createNotificationChannel"
# test3="notificationManager.notify"
# test4="NotificationManager"
# test5="onMessageReceived"
# test6="setPriority(NotificationCompat.PRIORITY_MAX)"
# test7="areNotificationsEnabled"
# test8="setPriority(NotificationCompat.PRIORITY_HIGH)"

# test9="NotificationCompat.Builder"
# test10="createNotificationChannel"
# test11="notificationManager.notify"
# test12="NotificationManager"
# test13="onMessageReceived"
# test14="setPriority(NotificationCompat.PRIORITY_MAX)"
# test15="areNotificationsEnabled"
# test16="setPriority(NotificationCompat.PRIORITY_HIGH)"
# test17="NotificationCompat.Builder"
# test18="createNotificationChannel"
# test19="notificationManager.notify"
# test20="NotificationManager"
# test21="onMessageReceived"
# test22="setPriority(NotificationCompat.PRIORITY_MAX)"
# test23="areNotificationsEnabled"
# test24="setPriority(NotificationCompat.PRIORITY_HIGH)"

#subs
# test1="getSubscriptionOfferDetails"
# test2="setSubscriptionUpdateParams"
# test3="setSubscriptionReplacementMode"
# #test4="BillingClient.consumeAsync"
# test4="^(?!.*\b(?:void|static|private|public)\s+consumeAsync\b).*consumeAsync.*"
# test5="setProductType(\"SUBS\")"
# test6="\"subs\""
# #test6="consumePurchase"
# test7="getPurchaseState"
# test8="^(?!.*\b(?:void|static|private|public)\s+ConsumeResponseListener\b).*ConsumeResponseListener.*"

test1="1154"
test2="1232"
test3="1319"
#test4="BillingClient.consumeAsync"
test4="912"
test5="910"
test6="584"
#test6="consumePurchase"
test7="1406"
test8="3104"



#reward file: "rewarded_lovin_maybe"
# test1="getoptionscontentviewgroup"
# test2="getrepeatinginterval"
# test3="getbodytextview"
# #test4="BillingClient.consumeAsync"
# test4="getcalltoactionbutton"
# test5="getfixedpositions"
# test6="geticoncontentview"
# #test6="consumePurchase"
# test7="getmainview"
# test8="getadvertisertextview"

#interstitial

# test1="features"
# test2="gettracingmode"
# test3="getcustomincludedcategories"
# #test4="BillingClient.consumeAsync"
# test4="getpredefinedcategories"
# test5="getvendorid"
# test6="getadvertisingid"
# #test6="consumePurchase"
# test7="onclosed"
# test8="countitems"




# test1="onConsumeResponse"
# test2=":consume"
# test3="IInAppBillingService.consumePurchase"
# #test4="BillingClient.consumeAsync"
# test4="consumeAsync"
# test5="setProductType(\"inapp\")"
# #test6="\"inapp\""
# test6="consumePurchase"
# test7="getPurchaseState"
# test8="ConsumeResponseListener"

test9="getSubscriptionOfferDetails"
test10="setSubscriptionUpdateParams"
test11="setSubscriptionReplacementMode"
test12="OneTimeProductNotification"
test13="ONE_TIME_PRODUCT_PURCHASED"
test14="New ONE_TIME_PRODUCT_CANCELED"
test15="PurchasesUpdatedListener"
test16="products.acknowledge"

test17="acknowledgementState"
test18="products.consume"
test19="notificationManager.notify"
test20="NotificationManager"
test21="IInAppBillingService.consumePurchase"
test22="BillingClient.consumeAsync"
test23="setProductType(\"inapp\")"
test24="\"inapp\""
#test24="setPriority(NotificationCompat.PRIORITY_HIGH)"

#offerwall_strigns=["airplay.startsmartwallad","airplay.startappwall","ironsource.showofferwall","ironsource.setofferwalllistener","showofferswall","showofferwalldialog","adtype.wall","openintegralwall","recommendwallsdk","showappoffers","showgameoffers","adwall","showappoffers","showappoffernoscore","openadwall","showkuguosprite","appdrivermanager"]
offerwall_strigns=["offerwall","public","airplay.startsmartwallad","airplay.startappwall","ironsource.showofferwall","ironsource.setofferwalllistener","showofferswall","showofferwalldialog","adtype.wall","openintegralwall","recommendwallsdk","showappoffers","showgameoffers","adwall","showappoffers","showappoffernoscore","openadwall","showkuguosprite","appdrivermanager"]



# test17="void dispatchdraw(canvas canvas)"
# test18="string getstring(string str)"
# test19="float getpivotx()"
# test20="float getpivoty()"
# test21="void enable()"
# test22="task start()"
# test23="int getoriginalpriority()"
# test24="string getticker()"

# test17="POST_NOTIFICATIONS"
# test18="firebasemessagingregistrar"
# test19="firebasemessagingservice"
# test20="permission.send"
# test21="intent.receive"
# test22="broadcastreceiver"
# test23="public int getoriginalpriority()"
# test24="public string getticker()"

notif_1="com.google.android.c2dm.intent.RECEIVE"
notif_2="com.google.firebase.messaging.FirebaseMessagingService"
notif_3="com.google.firebase.MESSAGING_EVENT"
notif_4="com.google.firebase.iid.FirebaseInstanceIdReceiver"
notif_t="android.permission.POST_NOTIFICATIONS"
notif_m="com.google.firebase.messaging"

"""compile regex for the test terms"""
test_one = re.compile(test1, re.IGNORECASE)
test_two = re.compile(test2, re.IGNORECASE)
test_three = re.compile(test3, re.IGNORECASE)
test_four = re.compile(test4, re.IGNORECASE)
test_five = re.compile(test5, re.IGNORECASE)
test_six = re.compile(test6, re.IGNORECASE)
test_seven = re.compile(test7,re.IGNORECASE)
test_eight = re.compile(test8,re.IGNORECASE)
test_nine = re.compile(test9)#, re.IGNORECASE)
test_ten = re.compile(test10)#, re.IGNORECASE)
test_eleven = re.compile(test11)#, re.IGNORECASE)
test_twelve = re.compile(test12)#, re.IGNORECASE)
test_thirteen = re.compile(test13)#, re.IGNORECASE)
test_fourteen = re.compile(test14)#, re.IGNORECASE)
test_fifteen = re.compile(test15)#,re.IGNORECASE)
test_sixteen = re.compile(test16)#,re.IGNORECASE)
test_seventeen = re.compile(test17)#), re.IGNORECASE)
test_eigteen = re.compile(test18)#, re.IGNORECASE)
test_nineteen = re.compile(test19)#, re.IGNORECASE)
test_twenty = re.compile(test20)#, re.IGNORECASE)
test_twentyone = re.compile(test21)#, re.IGNORECASE)
test_twentytwo = re.compile(test22)#, re.IGNORECASE)
test_twentrythree = re.compile(test23)#,re.IGNORECASE)
test_twentyfour = re.compile(test24)#,re.IGNORECASE)

"""compile regex for the terms used to detect various aspects"""
consummablePattern = re.compile("consume", re.IGNORECASE)

permanentPattern = re.compile("owned")
# permanentPattern=re.compile("startup")

subPattern = re.compile("subscribe")
#subPattern = re.compile("isautorenewing")

# rewardedPattern = re.compile("OnUserEarnedRewardListener")
#rewardedPattern = re.compile("onuserearnedrewardlistener")
# rewardedPattern = re.compile("label1044")

rewardedPattern = re.compile("earnedrewar.*")

InterPattern = re.compile("unityads")
removeAdPattern = re.compile("remove ads",re.IGNORECASE)

nativeAdsPattern = re.compile("AdSize\.BANNER")
nativeAdsPattern2 = re.compile("Adsize\.LARGE_BANNER")
nativeAdsPattern3 = re.compile("AdSize")

pushNotificationPattern = re.compile("android.permission.POST_NOTIFICATIONS")

leaderboardPattern = re.compile("getLeaderboardsClient")

offerwall_stuff = []
for a in offerwall_strigns:
	offerwall_stuff.append(re.compile(a))

	###################################################
# consummablePattern = re.compile("consumepurchase") #consumable purchase
# earnedPattern= re.compile("earnedreward") #rewarded ads
# subscribePattern=re.compile("isAutoRenewing") #subscription
# interstitialPattern=re.compile("onadshowedfullscreencontent") #interstitial ads
# InterPattern=re.compile("onadshowedfullscreencontent") #also interstitial ads
offerwallPattern=re.compile("offerwall") #offerwalls
# permanentIAP=re.compile("getpurchasestate") #non-consummable purchases
# notificationPattern=re.compile("createnotificationChannel") #push notification


@loguru_disable("androguard")
class Model:

	"""dictionary indicating the colors to be used in the graphic output depending on the value"""
	colors={
		False:"red",
		True:"green",
		3:"#fff" #others
	}


	list_applis=[]

	list_Truths={}
	filetrue="datasets/donnes_vrai_recent_secC.xlsx"

	""""Load the dataset of manually analyzed applications"""
	reals=Truths_final.Truth_final()
	list_truths_two=reals.loadTruth_final(filetrue)
	final_Truth = reals.getTruths_final()

	# reals_two=Truths_two.Truth_two()
	# reals_two.loadTruth_two("datasets/olds/Donnees_vraies_phase2_14_11_2024.xlsx")
	# list_Truths_two=reals_two.getTruths_two()

	list_Truths = final_Truth# | list_Truths_two

	#print("len all=",len(list_Truths),"len two=",len(list_Truths_two),"len one=",len(final_Truth))

	def getOtherApp(self,app):
		"""
		get the corresponding corresponding manually analyzed app

		:param app: application object, typically one resulting from the automated analysis
		:return: application object taken from list_Truths and containing the true values
		"""
		exist=False
		if (app.Title in self.list_Truths):
			exist = True
		elif (app.id in self.translation):
			app.Title = self.translation[app.id]
			if (app.Title in self.list_Truths):
				exist = True
			else:
				if(app.exist):
					print(app.Title, "was never found(getother) and exist  :(")

		if (exist):
			return self.list_Truths[app.Title]
		else:
			return None

	def __init__(self):
		self.listApplis=[]
		self.translation = loadTranslation("extra/all_free_ids_named_translation.txt", mode=0)
		self.translation_name_to_id = loadTranslation("extra/all_free_ids_named_translation.txt",mode=1)

	def getApplis(self):
		return self.list_applis

	def apps(self):
		return self.listApplis


#TODO: check if those gets can be used with getOtherApp
	def getGeneral(self):
		"""
		return the general data of the applications
		:return: the data
		"""
		general=[[], [], [], [], [], [], [], []]
		title=""
		for count in range(0,len(self.list_applis)):
			curr=self.list_applis[count].getData()["general"]
			general[0].append(curr[0]) #Name of the application
			general[1].append(curr[1])
			general[2].append(curr[2])
			general[3].append(curr[3])
			general[4].append(curr[4])
			general[5].append(curr[5])
			general[6].append(curr[6])
			general[7].append(curr[7])


		return general


	def getSocial(self):
		"""
		return the social data of the applications, include the comparison data
		:return:the data
		"""
		social=[[],[]]
		for count in range(0,len(self.list_applis)):
			tested=[]
			title=""
			exist=False
			curr=self.list_applis[count].getData()["social"]
			if(self.list_applis[count].Title in self.list_Truths):
				title=self.list_applis[count].Title
				exist=True
			elif(self.list_applis[count].id in self.translation):
				# if not found in list_Truths, try to look in the translation
				# Can happen in case of eg: mismatch between retrieved name
				title=self.translation[self.list_applis[count].id]
				exist=True
			# if(title in self.list_Truths):
			# 	exist=True
			else:
				exist=False #app never found
			if(exist):
				res = self.list_Truths[title]
				comp = self.list_applis[count].getComparision(res)
				tested.append(comp["social"][0])
				social[0].append([curr[0], self.colors[3]])
				social[1].append([curr[1], self.colors[tested[0]]])

			else:
				social[0].append([curr[0],self.colors[3]])
				social[1].append([curr[1], self.colors[3]])


		return social

	def calcPrecision(self,resultat):
		if(resultat[1]+resultat[3]==0):
			precision=-1
		else:
			precision= resultat[1] / (resultat[1] + resultat[3])
		return precision

	def calcRappel(self,resultats):
		if (resultats[1] + resultats[2] == 0):
			rappel = -1
		else:
			rappel = resultats[1] / (resultats[1] + resultats[2])
		return rappel


	def get_data_export(self):
		"""
		return the data's json
		:return: string
		"""
		jsony="{\"apps\":["
		#print(self.list_applis)
		for app in self.list_applis:
			x=("{"
			f'"UseUnity": "{str(app.UseUnity)}",'
			f'"Title" : "{str(app.Title)}",'
			f'"shownDeveloper" : "{str(app.shownDeveloper)}",'
			f'"developer" : "{str(app.developer)}",'
			f'"developerCountry" : "{str(app.developerCountry)}",'
			f'"publicationYear" : "{str(app.publicationYear)}",'
			f'"Downloads" : "{str(app.Downloads)}",'
			f'"Note" : "{str(app.Note)}",'
			f'"category" : "{str(app.category)}",'
			f'"ESRB" : "{str(app.ESRB)}",'
			f'"TeacherApproved" : "{str(app.TeacherApproved)}",'
			f'"iap_minPrice" : "{str(app.iap_minPrice)}",'
			f'"iap_maxPrice" : "{str(app.iap_maxPrice)}",'
			f'"PrivacyPolicy" : "{str(app.PrivacyPolicy)}",'

			f'"id" : "{str(app.id)}",'
			#f'"name" : "{str(app.name)}",'
			f'"consummableIAP" : "{str(app.consummableIAP)}",'
			f'"permanentIAP" : "{str(app.permanentIAP)}",'
			f'"subIAP" : "{str(app.subIAP)}",'

			f'"rewardedAds" : "{str(app.rewardedAds)}",'
			f'"interstitialAds" : "{str(app.interstitialAds)}",'
			f'"offerwall" : "{str(app.offerwall)}",'
			f'"nativeAds" : "{str(app.nativeAds)}",'
			f'"interactiveAds" : "{str(app.interactiveAds)}",'

			f'"push_notification" : "{str(app.push_notification)}",'

			f'"leaderboard" : "{str(app.leaderboard)}",'

			f'"removeAds" : "{str(app.removeAds)}",'

			f'"dateTest" : "{str(app.dateTest)}",'
			f'"recent" : "{str(app.recent)}",'

			f'"version" : "{str(app.version)}",'

			f'"url" : "{str(app.url)}",'
			f'"indicated_id" : "{str(app.indicated_id)}",'
			f'"test1" : "{str(app.test1)}",'
			f'"test2" : "{str(app.test2)}",'
			f'"test3" : "{str(app.test3)}",'
			f'"test4" : "{str(app.test4)}",'
			f'"test5" : "{str(app.test5)}",'
			f'"test6" : "{str(app.test6)}",'
			f'"test7" : "{str(app.test7)}",'
			f'"test8" : "{str(app.test8)}",'

			f'"test9" : "{str(app.test9)}",'
			f'"test10" : "{str(app.test10)}",'
			f'"test11" : "{str(app.test11)}",'
			f'"test12" : "{str(app.test12)}",'
			f'"test13" : "{str(app.test13)}",'
			f'"test14" : "{str(app.test14)}",'
			f'"test15" : "{str(app.test15)}",'
			f'"test16" : "{str(app.test16)}",'

			f'"test17" : "{str(app.test17)}",'
			f'"test18" : "{str(app.test18)}",'
			f'"test19" : "{str(app.test19)}",'
			f'"test20" : "{str(app.test20)}",'
			f'"test21" : "{str(app.test21)}",'
			f'"test22" : "{str(app.test22)}",'
			f'"test23" : "{str(app.test23)}",'
			f'"test24" : "{str(app.test24)}"')
			jsony = jsony + f'{x}'+"},"
		jsony=jsony[:-1]
		jsony = jsony + "]}"
		self.list_applis=[]
		return jsony

	def get_data_import(self,importation):
		"""
		Import the data from a json file
		:param importation: json file
		:return: nothing
		"""
		data=json.loads(importation)
		for applications in data['apps']:
			appli=application.application()
			appli.UseUnity = applications['UseUnity']

			appli.Title = applications['Title']

			appli.shownDeveloper = applications['shownDeveloper']
			appli.developer = applications['developer']
			appli.developerCountry = applications['developerCountry']
			appli.publicationYear = str(applications['publicationYear'])
			appli.Downloads = applications['Downloads']
			appli.Note = applications['Note']
			appli.category = applications['category']
			appli.ESRB = applications['ESRB']
			appli.TeacherApproved = applications['TeacherApproved']
			appli.iap_minPrice = float(applications['iap_minPrice'])
			appli.iap_maxPrice = float(applications['iap_maxPrice'])

			appli.PrivacyPolicy = bool(applications['PrivacyPolicy'])

			appli.id = applications['id']
			#appli.name = applications['name']
			appli.name = "ABCD"
			appli.consummableIAP = strToBool(applications['consummableIAP'])
			#print(appli.name,appli.consummableIAP)
			appli.permanentIAP = strToBool(applications['permanentIAP'])
			appli.subIAP = strToBool(applications['subIAP'])

			appli.rewardedAds = strToBool(applications['rewardedAds'])
			appli.interstitialAds = strToBool(applications['interstitialAds'])
			appli.offerwall = strToBool(applications['offerwall'])
			appli.nativeAds = strToBool(applications['nativeAds'])
			appli.interactiveAds = strToBool(applications['interactiveAds'])

			appli.push_notification = strToBool(applications['push_notification'])

			appli.leaderboard = strToBool(applications['leaderboard'])

			appli.removeAds = strToBool(applications['removeAds'])

			appli.dateTest = applications['dateTest']
			appli.recent = str(applications['recent'])

			appli.version = applications['version']

			appli.url = ""
			appli.indicated_id = applications['indicated_id']
			appli.test1 = strToBool(applications['test1'])
			appli.test2 = strToBool(applications['test2'])
			appli.test3 = strToBool(applications['test3'])
			appli.test4 = strToBool(applications['test4'])
			appli.test5 = strToBool(applications['test5'])
			appli.test6 = strToBool(applications['test6'])
			appli.test7 = strToBool(applications['test7'])
			appli.test8 = strToBool(applications['test8'])

			appli.test9 = strToBool(applications['test9'])
			appli.test10 = strToBool(applications['test10'])
			appli.test11 = strToBool(applications['test11'])
			appli.test12 = strToBool(applications['test12'])
			appli.test13 = strToBool(applications['test13'])
			appli.test14 = strToBool(applications['test14'])
			appli.test15 = strToBool(applications['test15'])
			appli.test16 = strToBool(applications['test16'])

			appli.test17 = strToBool(applications['test17'])
			appli.test18 = strToBool(applications['test18'])
			appli.test19 = strToBool(applications['test19'])
			appli.test20 = strToBool(applications['test20'])
			appli.test21 = strToBool(applications['test21'])
			appli.test22 = strToBool(applications['test22'])
			appli.test23 = strToBool(applications['test23'])
			appli.test24 = strToBool(applications['test24'])
			self.list_applis.append(appli)


	def getIAP(self):
		"""
		return the microtransaction data of the applications, include the comparison data
		:return:the data
		"""
		iap = [[], [], [], [], []]
		for count in range(0, len(self.list_applis)):
			tested=[]
			title=""
			exist=False
			curr=self.list_applis[count].getData()["IAP"]
			if(self.list_applis[count].Title in self.list_Truths):
				title=self.list_applis[count].Title
				#exist=True
			elif(self.list_applis[count].id in self.translation):
				title=self.translation[self.list_applis[count].id]

			if(title in self.list_Truths):
				exist=True
			else:
				exist=False
				print("don't exist",title)
			if(exist):
				res = self.list_Truths[title]
				comp = self.list_applis[count].getComparision(res)
				tested.append(comp["IAP"][0])
				tested.append(comp["IAP"][1])
				tested.append(comp["IAP"][2])
				tested.append(comp["IAP"][3])
				iap[0].append([curr[0], self.colors[3]])
				iap[1].append([curr[1], self.colors[tested[0]]])
				iap[2].append([curr[2], self.colors[tested[1]]])
				iap[3].append([curr[3], self.colors[tested[2]]])
				iap[4].append([curr[4], self.colors[tested[3]]])

			else:
				iap[0].append([curr[0], self.colors[3]])
				iap[1].append([curr[1], self.colors[3]])
				iap[2].append([curr[2], self.colors[3]])
				iap[3].append([curr[3], self.colors[3]])
				iap[4].append([curr[4], self.colors[3]])
		return iap

	def getTest(self):
		"""
		return the test1 data of the applications, include the comparison data
		:return:the data
		"""
		test = [[], [], [], [],[],[],[],[],[]]
		for count in range(0, len(self.list_applis)):
			tested = []
			exist = False
			title=""
			curr = self.list_applis[count].getData()["test"]
			id = self.list_applis[count].id
			if (self.list_applis[count].Title in self.list_Truths):
				title = self.list_applis[count].Title
			elif (self.list_applis[count].id in self.translation):
				title = self.translation[self.list_applis[count].id]
			if(title in self.list_Truths):
				exist=True
			else:
				exist=False
			if (exist):
				res = self.list_Truths[title]
				comp = self.list_applis[count].getComparision(res)

				tested.append(comp["test"][0])
				tested.append(comp["test"][1])
				tested.append(comp["test"][2])
				tested.append(comp["test"][3])
				tested.append(comp["test"][4])
				tested.append(comp["test"][5])
				tested.append(comp["test"][6])
				tested.append(comp["test"][7])

				test[0].append([curr[0], self.colors[3]])
				#test[0].append([id,self.colors[3]])
				test[1].append([curr[1], self.colors[tested[0]]])
				test[2].append([curr[2], self.colors[tested[1]]])
				test[3].append([curr[3], self.colors[tested[2]]])
				test[4].append([curr[4], self.colors[tested[3]]])
				test[5].append([curr[5], self.colors[tested[4]]])
				test[6].append([curr[6], self.colors[tested[5]]])
				test[7].append([curr[7], self.colors[tested[6]]])
				test[8].append([curr[8], self.colors[tested[7]]])

			else:
				test[0].append([curr[0], self.colors[3]])
				test[1].append([curr[1], self.colors[3]])
				test[2].append([curr[2], self.colors[3]])
				test[3].append([curr[3], self.colors[3]])
				test[4].append([curr[4], self.colors[3]])
				test[5].append([curr[5], self.colors[3]])
				test[6].append([curr[6], self.colors[3]])
				test[7].append([curr[7], self.colors[3]])
				test[8].append([curr[8], self.colors[3]])

		return test

	def getTest2(self):
		"""
		return the test2 data of the applications, include the comparison data
		:return:the data
		"""
		test = [[], [], [], [],[],[],[],[],[]]
		for count in range(0, len(self.list_applis)):
			tested = []
			exist = False
			title=""
			curr = self.list_applis[count].getData()["test2"]
			if (self.list_applis[count].Title in self.list_Truths):
				title = self.list_applis[count].Title
			elif (self.list_applis[count].id in self.translation):
				title = self.translation[self.list_applis[count].id]
			if(title in self.list_Truths):
				exist=True
			else:
				exist=False
			if (exist):
				res = self.list_Truths[title]
				comp = self.list_applis[count].getComparision(res)

				tested.append(comp["test2"][0])
				tested.append(comp["test2"][1])
				tested.append(comp["test2"][2])
				tested.append(comp["test2"][3])
				tested.append(comp["test2"][4])
				tested.append(comp["test2"][5])
				tested.append(comp["test2"][6])
				tested.append(comp["test2"][7])

				test[0].append([curr[0], self.colors[3]])
				test[1].append([curr[1], self.colors[tested[0]]])
				test[2].append([curr[2], self.colors[tested[1]]])
				test[3].append([curr[3], self.colors[tested[2]]])
				test[4].append([curr[4], self.colors[tested[3]]])
				test[5].append([curr[5], self.colors[tested[4]]])
				test[6].append([curr[6], self.colors[tested[5]]])
				test[7].append([curr[7], self.colors[tested[6]]])
				test[8].append([curr[8], self.colors[tested[7]]])

			else:
				test[0].append([curr[0], self.colors[3]])
				test[1].append([curr[1], self.colors[3]])
				test[2].append([curr[2], self.colors[3]])
				test[3].append([curr[3], self.colors[3]])
				test[4].append([curr[4], self.colors[3]])
				test[5].append([curr[5], self.colors[3]])
				test[6].append([curr[6], self.colors[3]])
				test[7].append([curr[7], self.colors[3]])
				test[8].append([curr[8], self.colors[3]])

		return test

	def getTest3(self):
		"""
		return the test3 data of the applications, include the comparison data
		:return:the data
		"""
		test = [[], [], [], [],[],[],[],[],[]]
		for count in range(0, len(self.list_applis)):
			tested = []
			exist = False
			title=""
			curr = self.list_applis[count].getData()["test3"]
			id=self.list_applis[count].id
			if (self.list_applis[count].Title in self.list_Truths):
				title = self.list_applis[count].Title
			elif (self.list_applis[count].id in self.translation):
				title = self.translation[self.list_applis[count].id]
			if(title in self.list_Truths):
				exist=True
			else:
				exist=False
			if (exist):
				res = self.list_Truths[title]
				comp = self.list_applis[count].getComparision(res)

				tested.append(comp["test3"][0])
				tested.append(comp["test3"][1])
				tested.append(comp["test3"][2])
				tested.append(comp["test3"][3])
				tested.append(comp["test3"][4])
				tested.append(comp["test3"][5])
				tested.append(comp["test3"][6])
				tested.append(comp["test3"][7])

				#test[0].append([curr[0], self.colors[3]])
				test[0].append([id,self.colors[3]])
				test[1].append([curr[1], self.colors[tested[0]]])
				test[2].append([curr[2], self.colors[tested[1]]])
				test[3].append([curr[3], self.colors[tested[2]]])
				test[4].append([curr[4], self.colors[tested[3]]])
				test[5].append([curr[5], self.colors[tested[4]]])
				test[6].append([curr[6], self.colors[tested[5]]])
				test[7].append([curr[7], self.colors[tested[6]]])
				test[8].append([curr[8], self.colors[tested[7]]])

			else:
				test[0].append([curr[0], self.colors[3]])
				test[1].append([curr[1], self.colors[3]])
				test[2].append([curr[2], self.colors[3]])
				test[3].append([curr[3], self.colors[3]])
				test[4].append([curr[4], self.colors[3]])
				test[5].append([curr[5], self.colors[3]])
				test[6].append([curr[6], self.colors[3]])
				test[7].append([curr[7], self.colors[3]])
				test[8].append([curr[8], self.colors[3]])

		return test

	# def getIAPStat(self):
	# 	#name,precision,rappel
	# 	stater=[[],[],[]]
	# 	for count in range(0,len(self.list_applis)):
	# 		#print(self.list_applis[count].Title)
	# 		if (self.list_applis[count].Title in self.list_Truths):
	# 			#TODO: else for when app isn't in truth file
	# 			res = self.list_Truths[self.list_applis[count].Title]
	# 			curr=self.list_applis[count].getIAPStat(res)
	#
	# 			stater[0].append(self.list_applis[count].Title)
	# 			stater[1].append(self.calcPrecision(curr))
	# 			stater[2].append(self.calcRappel(curr))
	# 	return stater
	#
	# def getSocialStat(self):
	# 	#name,precision,rappel
	# 	statery=[[],[],[]]
	# 	for count in range(0,len(self.list_applis)):
	# 		#print(self.list_applis[count].Title)
	# 		if (self.list_applis[count].Title in self.list_Truths):
	# 			res = self.list_Truths[self.list_applis[count].Title]
	# 		#if (self.list_applis[count].Title in self.list_Truths):
	# 			curr=self.list_applis[count].getSocialStat(res)
	# 			statery[0].append(self.list_applis[count].Title)
	# 			statery[1].append(self.calcPrecision(curr))
	# 			statery[2].append(self.calcRappel(curr))
	# 	return statery
	#
	# def getAdsStat(self):
	# 	stats=[[],[],[],[],[]]
	# 	#name,precision,rappel
	# 	stater=[[],[],[]]
	# 	for count in range(0,len(self.list_applis)):
	# 		#print(self.list_applis[count].Title)
	# 		if (self.list_applis[count].Title in self.list_Truths):
	# 			res = self.list_Truths[self.list_applis[count].Title]
	# 		#if (self.list_applis[count].Title in self.list_Truths):
	# 			curr=self.list_applis[count].getAdsStat(res)
	# 			stater[0].append(self.list_applis[count].Title)
	# 			stater[1].append(self.calcPrecision(curr))
	# 			stater[2].append(self.calcRappel(curr))
	# 	return stater
	#
	# def getStructureStat(self):
	# 	stats=[[],[],[],[],[]]
	# 	#name,precision,rappel
	# 	stater=[[],[],[]]
	# 	for count in range(0,len(self.list_applis)):
	# 		#print(self.list_applis[count].Title)
	# 		if (self.list_applis[count].Title in self.list_Truths):
	# 			res = self.list_Truths[self.list_applis[count].Title]
	# 		#if (self.list_applis[count].Title in self.list_Truths):
	# 			curr=self.list_applis[count].getStructureStat(res)
	# 			stater[0].append(self.list_applis[count].Title)
	# 			stater[1].append(self.calcPrecision(curr))
	# 			stater[2].append(self.calcRappel(curr))
	# 	return stater
	#
	# # def getTestStat(self):
	# # 	stats=[[],[],[],[],[],[]]
	# # 	stater=[[],[],[]]
	# # 	for count in range(0,len(self.list_applis)):
	# # 		res=self.list_Truths[self.list_applis[count].Title]
	# # 		curr=self.list_applis[count].getTestStat(test)
	# # 		stater[0].append(self.list_applis[count].Title)
	# # 		stater[1].append(self.calcPrecision(curr))
	# # 		stater[2].append(self.calcRappel(curr))
	#
	#
	# def getAdsT(self):
	# 	ads = [[], [], [], []]
	# 	for count in range(0, len(self.list_applis)):
	# 		curr = self.list_applis[count].getData()["ads"]
	# 		ads[0].append(curr[0])
	# 		ads[1].append(curr[1])
	# 		ads[2].append(curr[2])
	# 		ads[3].append(curr[3])
	# 	return ads

	def getAds(self):
		"""
		return the advertisement data of the applications, include the comparison data
		:return:the data
		"""
		ads = [[], [], [], [],[]]
		for count in range(0, len(self.list_applis)):
			tested=[]
			exist=False
			title=""
			curr=self.list_applis[count].getData()["ads"]
			if(self.list_applis[count].Title in self.list_Truths):
				title=self.list_applis[count].Title
			#	exist=True
			elif(self.list_applis[count].id in self.translation):
				title=self.translation[self.list_applis[count].id]
			#	exist=True
			if(title in self.list_Truths):
				exist=True
			else:
				exist=False
			if(exist):
				res = self.list_Truths[title]
				comp=self.list_applis[count].getComparision(res)
				tested.append(comp["ads"][0])
				tested.append(comp["ads"][1])
				tested.append(comp["ads"][2])
				tested.append(comp["ads"][3])
				ads[0].append([curr[0],self.colors[3]])
				ads[1].append([curr[1], self.colors[tested[0]]])
				ads[2].append([curr[2], self.colors[tested[1]]])
				ads[3].append([curr[3], self.colors[tested[2]]])
				ads[4].append([curr[4], self.colors[tested[3]]])

			else:
				ads[0].append([curr[0],self.colors[3]])
				ads[1].append([curr[1],self.colors[3]])
				ads[2].append([curr[2],self.colors[3]])
				ads[3].append([curr[3],self.colors[3]])
				ads[4].append([curr[4],self.colors[3]])
		return ads

	def getStructure(self):
		"""
		return the structure data of the applications, include the comparison data
		:return:the data
		"""
		structure=[[],[]]
		for count in range(0,len(self.list_applis)):
			tested=[]
			exist=False
			title=""
			curr=self.list_applis[count].getData()["structure"]
			if(self.list_applis[count].Title in self.list_Truths):
				title=self.list_applis[count].Title
			#	exist=True
			elif(self.list_applis[count].id in self.translation):
				title=self.translation[self.list_applis[count].id]
			#	exist=True

			if(title in self.list_Truths):
				exist=True
			else:
				exist=False
			if(exist):
				res=self.list_Truths[title]
				comp=self.list_applis[count].getComparision(res)
				tested.append(comp["structure"][0])
				structure[0].append([curr[0],self.colors[3]])
				structure[1].append([curr[1],self.colors[tested[0]]])
			else:
				structure[0].append([curr[0], self.colors[3]])
				structure[1].append([curr[1], self.colors[3]])
		return structure



	def analyse_single(self,folder, linux):
		# excluding=".*billingclient.*\.java"
		# exclude=re.compile(excluding, re.IGNORECASE)
		#
		# moreexclude=".*android.*"
		# ugh=re.compile(moreexclude,re.IGNORECASE)

		"""
		analyse a single application
		:param folder: folder containing the source code and the resources of the application
		:param linux: boolean indicating if it's called from a linux machine or a windows machine
			file path format is different
		:return: application object with the predicted values
		"""
		global jadx #was this decompiled with jadx
		global file_count #total number of files in the datasets(used to give progress)
		global file_done #total number of files already analyzed

		result = application.application()
		result.name = folder
		notification_perm=False
		filery=False #should the results be saved in a file?
			#save, if aspect is detected, the pathfile, the name of the application and the line that raised the flag

		if filery==True:
			fileRew=open("TestResultFiles/spec/Filerewarded.txt", "a+", encoding="utf-8")
			fileCon = open("TestResultFiles/spec/Fileconsummable.txt", "a+", encoding="utf-8")
			filePerm=open("TestResultFiles/spec/Filepermanent.txt", "a+", encoding="utf-8")
			fileInterOne=open("TestResultFiles/spec/Fileinterstitial_one.txt", "a+", encoding="utf-8")
			fileInterTwo=open("TestResultFiles/spec/Fileinterstitial_two.txt", "a+", encoding="utf-8")
			fileIAP = open("TestResultFiles/spec/Fileiap.txt", "a+", encoding="utf-8")
			fileLeader=open("TestResultFiles/spec/FileLeader.txt","a+",encoding="utf-8")
			fileRemoveAds=open("TestResultFiles/spec/FileRemoveAds.txt","a+",encoding="utf-8")

			fileTestOne=open("TestResultFiles/one/good/fileTestOne.txt", "a+", encoding="utf-8")
			fileTestTwo=open("TestResultFiles/one/good/fileTestTwo.txt", "a+", encoding="utf-8")
			fileTestThree=open("TestResultFiles/one/good/fileTestThree.txt", "a+", encoding="utf-8")
			fileTestFour=open("TestResultFiles/one/good/fileTestFour.txt", "a+", encoding="utf-8")
			fileTestFive=open("TestResultFiles/one/good/fileTestFive.txt", "a+", encoding="utf-8")
			fileTestSix=open("TestResultFiles/one/good/fileTestSix.txt", "a+", encoding="utf-8")
			fileTestSeven=open("TestResultFiles/one/good/fileTestSeven.txt", "a+", encoding="utf-8")
			fileTestEight=open("TestResultFiles/one/good/fileTestEight.txt", "a+", encoding="utf-8")
			fileTestOneBad = open("TestResultFiles/one/bad/fileTestOne.txt", "a+", encoding="utf-8")
			fileTestTwoBad  = open("TestResultFiles/one/bad/fileTestTwo.txt", "a+", encoding="utf-8")
			fileTestThreeBad  = open("TestResultFiles/one/bad/fileTestThree.txt", "a+", encoding="utf-8")
			fileTestFourBad  = open("TestResultFiles/one/bad/fileTestFour.txt", "a+", encoding="utf-8")
			fileTestFiveBad  = open("TestResultFiles/one/bad/fileTestFive.txt", "a+", encoding="utf-8")
			fileTestSixBad  = open("TestResultFiles/one/bad/fileTestSix.txt", "a+", encoding="utf-8")
			fileTestSevenBad  = open("TestResultFiles/one/bad/fileTestSeven.txt", "a+", encoding="utf-8")
			fileTestEightBad  = open("TestResultFiles/one/bad/fileTestEight.txt", "a+", encoding="utf-8")

			fileTestOneb =open("TestResultFiles/two/good/fileTestOne.txt", "a+", encoding="utf-8")
			fileTestTwob =open("TestResultFiles/two/good/fileTestTwo.txt", "a+", encoding="utf-8")
			fileTestThreeb =open("TestResultFiles/two/good/fileTestThree.txt", "a+", encoding="utf-8")
			fileTestFourb =open("TestResultFiles/two/good/fileTestFour.txt", "a+", encoding="utf-8")
			fileTestFiveb =open("TestResultFiles/two/good/fileTestFive.txt", "a+", encoding="utf-8")
			fileTestSixb =open("TestResultFiles/two/good/fileTestSix.txt", "a+", encoding="utf-8")
			fileTestSevenb =open("TestResultFiles/two/good/fileTestSeven.txt", "a+", encoding="utf-8")
			fileTestEightb =open("TestResultFiles/two/good/fileTestEight.txt", "a+", encoding="utf-8")
			fileTestOnebBad =open("TestResultFiles/two/bad/fileTestOne.txt", "a+", encoding="utf-8")
			fileTestTwobBad =open("TestResultFiles/two/bad/fileTestTwo.txt", "a+", encoding="utf-8")
			fileTestThreebBad =open("TestResultFiles/two/bad/fileTestThree.txt", "a+", encoding="utf-8")
			fileTestFourbBad =open("TestResultFiles/two/bad/fileTestFour.txt", "a+", encoding="utf-8")
			fileTestFivebBad =open("TestResultFiles/two/bad/fileTestFive.txt", "a+", encoding="utf-8")
			fileTestSixbBad =open("TestResultFiles/two/bad/fileTestSix.txt", "a+", encoding="utf-8")
			fileTestSevenbBad =open("TestResultFiles/two/bad/fileTestSeven.txt", "a+", encoding="utf-8")
			fileTestEightbBad =open("TestResultFiles/two/bad/fileTestEight.txt", "a+", encoding="utf-8")

			fileTestOnec =open("TestResultFiles/three/good/fileTestOne.txt", "a+", encoding="utf-8")
			fileTestTwoc =open("TestResultFiles/three/good/fileTestTwo.txt", "a+", encoding="utf-8")
			fileTestThreec =open("TestResultFiles/three/good/fileTestThree.txt", "a+", encoding="utf-8")
			fileTestFourc =open("TestResultFiles/three/good/fileTestFour.txt", "a+", encoding="utf-8")
			fileTestFivec =open("TestResultFiles/three/good/fileTestFive.txt", "a+", encoding="utf-8")
			fileTestSixc =open("TestResultFiles/three/good/fileTestSix.txt", "a+", encoding="utf-8")
			fileTestSevenc =open("TestResultFiles/three/good/fileTestSeven.txt", "a+", encoding="utf-8")
			fileTestEightc =open("TestResultFiles/three/good/fileTestEight.txt", "a+", encoding="utf-8")
			fileTestOnecBad =open("TestResultFiles/three/bad/fileTestOne.txt", "a+", encoding="utf-8")
			fileTestTwocBad =open("TestResultFiles/three/bad/fileTestTwo.txt", "a+", encoding="utf-8")
			fileTestThreecBad =open("TestResultFiles/three/bad/fileTestThree.txt", "a+", encoding="utf-8")
			fileTestFourcBad =open("TestResultFiles/three/bad/fileTestFour.txt", "a+", encoding="utf-8")
			fileTestFivecBad =open("TestResultFiles/three/bad/fileTestFive.txt", "a+", encoding="utf-8")
			fileTestSixcBad =open("TestResultFiles/three/bad/fileTestSix.txt", "a+", encoding="utf-8")
			fileTestSevencBad =open("TestResultFiles/three/bad/fileTestSeven.txt", "a+", encoding="utf-8")
			fileTestEightcBad =open("TestResultFiles/three/bad/fileTestEight.txt", "a+", encoding="utf-8")

		if(jadx): #set the relevant file paths
			if (linux):
				manExtension = "/resources/AndroidManifest.xml"
				decExtension = "/sources"
				#decExtension = "/exp"
				unpackExtension = "/resources/res/layout"
			else:
				manExtension = "\\resources\\AndroidManifest.xml"
				decExtension = "\\sources"
				#decExtension = "\\exp"
				unpackExtension = "\\resources"
		else:
			if(linux):
				manExtension="/unpacked/AndroidManifest.xml"
				decExtension="/decompiled"
				unpackExtension="/unpacked"
			else:
				manExtension="\\unpacked\\AndroidManifest.xml"
				decExtension = "\\decompiled"
				unpackExtension = "\\unpacked"

		#old patterns, ignore

		#consummablePattern = re.compile("purchase_history", re.IGNORECASE)
		#consummablePattern = re.compile("utility22", re.IGNORECASE)
		# offerwall_stuff=[]
		# for a in offerwall_strigns:
		# 	offerwall_stuff.append(re.compile(a))
		# consummablePattern = re.compile("com_facebook_login_button_transparency", re.IGNORECASE)
		#
		# permanentPattern=re.compile("owned")
		# #permanentPattern=re.compile("startup")
		#
		# subPattern = re.compile("isAutoRenewing")
		#
		# #rewardedPattern = re.compile("OnUserEarnedRewardListener")
		# rewardedPattern = re.compile("onuserearnedrewardlistener")
		# #rewardedPattern = re.compile("label1044")
		#
		# #rewardedPattern = re.compile("EarnedRewar. *")
		# #InterPattern = re.compile("InterstitialAd")
		#
		# InterPattern = re.compile("unityads")
		# #InterPattern = re.compile("image_provider_uris")
		# #offerwallPattern = re.compile("offerwall")
		# #offerwallPattern = re.compile("(airplay\.startsmartwallad|airplay\.startappwall|ironsource\.showofferwall|ironsource\.setofferwalllistener|showofferswall|showofferwalldialog|adtype\.wall|openintegralwall|recommendwallsdk|showappoffers|showgameoffers|adwall|showappoffers|showappoffernoscore|openadwall|showkuguosprite|appdrivermanager\(\))")
		# #offerwallPattern = re.compile("origins") #for interstitial
		#
		#
		# nativeAdsPattern = re.compile("AdSize\.BANNER")
		# nativeAdsPattern2 = re.compile("Adsize\.LARGE_BANNER")
		# nativeAdsPattern3= re.compile("AdSize")
		#
		# pushNotificationPattern = re.compile("android.permission.POST_NOTIFICATIONS")
		# #
		#
		# leaderboardPattern = re.compile("getLeaderboardsClient")

		#test_one = re.compile("u0001ji", re.IGNORECASE)
		#test_two = re.compile("newinstance3", re.IGNORECASE)
		#test_three = re.compile("newinstance4", re.IGNORECASE)
		#test_four = re.compile("tagnumber", re.IGNORECASE)
		#test_five = re.compile("34866", re.IGNORECASE)
		#test_six = re.compile("34867", re.IGNORECASE)
		#test_seven = re.compile("httpresponse22",re.IGNORECASE)
		#test_eight = re.compile("androidcontext",re.IGNORECASE)

		# test_one = re.compile(test1, re.IGNORECASE)
		# test_two = re.compile(test2, re.IGNORECASE)
		# test_three = re.compile(test3, re.IGNORECASE)
		# test_four = re.compile(test4, re.IGNORECASE)
		# test_five = re.compile(test5, re.IGNORECASE)
		# test_six = re.compile(test6, re.IGNORECASE)
		# test_seven = re.compile(test7,re.IGNORECASE)
		# test_eight = re.compile(test8,re.IGNORECASE)
		# test_nine = re.compile(test9, re.IGNORECASE)
		# test_ten = re.compile(test10, re.IGNORECASE)
		# test_eleven = re.compile(test11, re.IGNORECASE)
		# test_twelve = re.compile(test12, re.IGNORECASE)
		# test_thirteen = re.compile(test13, re.IGNORECASE)
		# test_fourteen = re.compile(test14, re.IGNORECASE)
		# test_fifteen = re.compile(test15,re.IGNORECASE)
		# test_sixteen = re.compile(test16,re.IGNORECASE)
		# test_seventeen = re.compile(test17, re.IGNORECASE)
		# test_eigteen = re.compile(test18, re.IGNORECASE)
		# test_nineteen = re.compile(test19, re.IGNORECASE)
		# test_twenty = re.compile(test20, re.IGNORECASE)
		# test_twentyone = re.compile(test21, re.IGNORECASE)
		# test_twentytwo = re.compile(test22, re.IGNORECASE)
		# test_twentrythree = re.compile(test23,re.IGNORECASE)
		# test_twentyfour = re.compile(test24,re.IGNORECASE)


		# get app ID
		#manifest = open(folder + "\\unpacked\\AndroidManifest.xml")
		#print(folder+manExtension)
		#manifest = open(folder + manExtension, encoding='utf8')
		#print("before",folder,manExtension)
		huh=folder+manExtension
		test=os.path.isfile(huh)
		#if test:
			#result.exist=True
		try:
			fileName=folder+manExtension
			#print("inside",folder,manExtension)
			manifest = open(folder + manExtension,encoding='utf8')
			man=manifest.read()
			position_first = man.find("package=\"") + 9
			position_last = man.find("\"", position_first)
			result.id = man[position_first:position_last]
			#get app id
			GetStoreInfo(result)
			manifest.close()
		except:
			print("ID(",result.id,") from manifest couldn't be retrieved in",fileName)
		#else:
		#	print("why?????",huh)

		FCM_pos=False
		not_pos=False
		if(os.path.exists(folder+manExtension)):
			with open(folder+manExtension,encoding="cp437") as manFile:
				# #look for push notification
				man = manFile.read()
				# print(result.id,result.Title)
				if notif_m in man:
					not_pos=True
				elif (notif_1 in man) or (notif_2 in man) or(notif_3 in man) or (notif_4 in man):
					not_pos=True
				if (notif_1 in man) and (notif_2 in man) and (notif_3 in man) and (notif_4 in man):
					fcm=True
					#result.push_notification=True
				if "onMessageReceived" not in man and not_pos==True:
					result.pushFCM=True
				if (not ("android.permission.POST_NOTIFICATIONS" in man)):
				#if ("android.permission.POST_NOTIFICATIONS" in man):
					result.push_notification=False
					#result.push_notification = True
					notification_perm=True
			# if "privacy" in man:
			# 	result.PrivacyPolicy=True

			manifest.close()

		other = Model.getOtherApp(self, result)
		if other is not None:
			checkTest1 = (other.consummableIAP)  # or other.consummableIAP)
			# checkTest2=(other.subIAP)# or other.consummableIAP)
			# checkTest3=(other.subIAP)# or other.consummableIAP)
		else:
			filing=False

		# analyse files
		#if(False):
		for (root, dirs, files) in os.walk((folder + decExtension), topdown=True):
		#for (root, dirs, files) in os.walk((folder + unpackExtension), topdown=True):
			for filer in files:
				filing=filery
				if(linux):
					checking = root + "/" + filer
				else:
					checking = root + "\\" + filer
				#if(filer=='strings.xml'):
				#if(filer.endswith('.xml')):
				#if(filer=='R.java'):
				#if(filer.endswith('.java')):
				#if(False):
				#mustcheck=exclude.search(checking)
				#alsocheck=ugh.search(checking)

				if(True):# and (not mustcheck)):# and (not alsocheck)):
					file_one = open(checking, encoding="cp437")
					line=file_one.read()
					# quicky=file_one.read()
					#context_one=file_one.readlines()
					# # abc=file_one.read()
					# # #content= extract_code_block(abc)
					# #sku_types=defaultdict(set)
					# #sku_usage=defaultdict(list)
					# # for match in sku_pattern.finditer(file_one):
					# # 	sku=match.group(1)
					#
					# if subs_type_pattern_sku.search(quicky):
					# 	result.subIAP=True
					# if consume_pattern_sku.search(quicky):
					# 	result.consummableIAP=True
					# if persist_pattern_sku.search(quicky):
					# 	result.permanentIAP=True

					# line=file_one.read()
					# #for i, line in enumerate(context_one):
					# 	# for i,line in enumerate(file_one):
					# 	# print(line)
					# 	# for line in content:
					# 	# print("===============")
					# 	# print(line)
					# 	# print("===============")
					# 	# line = line.lower()
					# 	# line.strip()
					# 	# if(True):
					#
					# 	#context = getContext(i, context_one)
					# if not (result.consummableIAP):  # and (not "api" in checking) and (not "google" in checking) and (not "IInAppBillingService" in checking)):
					# 	if consummablePattern.search(line):
					# 		result.consummableIAP = True
					#
					# if not result.subIAP:
					# 	# if True:
					# 	if subPattern.search(line):
					# 		#	fileIAP.write(result.Title+"=(subscription)="+line+" in" +checking+"\n")
					# 		result.subIAP = True
					#
					# if not result.permanentIAP:
					# 	if permanentPattern.search(line):
					# 		# print(game,"=",line,"in ",checking)
					# 		#	filePerm.write(result.Title+ "=(permanent)="+ line+ " in "+ checking + "\n")
					# 		result.permanentIAP = True
					#
					#
					# if not (result.rewardedAds):
					# 	if rewardedPattern.search(line):
					# 		#	fileRew.write(result.Title+"=(rewarded)="+line+" in "+checking+"\n")
					# 		result.rewardedAds = True
					#
					#
					# if not result.interstitialAds:
					# 	if InterPattern.search(line):
					# 		result.interstitialAds = True
					#
					# if not result.removeAds:
					# 	if removeAdPattern.search(line):
					# 		result.removeAds=True
					#
					# # if(False):
					# if not result.offerwall:
					# 	if a.search(line):
					# 		result.offerwall = True
					#
					# # if(False):
					# if not result.nativeAds:
					# 	if nativeAdsPattern.search(line) or nativeAdsPattern3.search(line):
					# 		# fileADS.write(result.Title+ "=(native)="+ line+ " in "+ checking + "\n")
					# 		result.nativeAds = True
					#
					#
					# # if(False):
					# if not result.leaderboard:
					# 	if leaderboardPattern.search(line):
					# 		result.leaderboard = True
					#
					# # ####################################
					# # if True:
					# if not result.test1:
					# 	if test_one.search(line):
					# 		result.test1 = True
					#
					#
					# # if True:
					# if not result.test2:
					# 	if test_two.search(line):
					# 		result.test2 = True
					#
					#
					# # if True:
					# if not result.test3:
					# 	if test_three.search(line):
					# 		result.test3 = True
					#
					#
					# # if True:
					# if not result.test4:
					# 	if test_four.search(line):
					# 		result.test4 = True
					#
					# # if True:
					# if not result.test5:
					# 	if test_five.search(line):
					# 		result.test5 = True
					#
					# # if True:
					# if not result.test6:
					# 	if test_six.search(line):
					# 		result.test6 = True
					#
					# # if True:
					# if not result.test7:
					# 	if test_seven.search(line):
					# 		result.test7 = True
					#
					# # if True:
					# if not result.test8:
					# 	if test_eight.search(line):
					# 		result.test8 = True
					#
					# if True:
					# if not result.test9:
					# 	if test_nine.search(line):
					# 		result.test9 = True
					#
					# # if True:
					# if not result.test10:
					# 	if test_ten.search(line):
					# 		result.test10 = True
					#
					# # if True:
					# if not result.test11:
					# 	if test_eleven.search(line):
					# 		result.test11 = True
					#
					# # if True:
					# if not result.test12:
					# 	if test_twelve.search(line):
					# 		result.test12 = True
					#
					# # if True:
					# if not result.test13:
					# 	if test_thirteen.search(line):
					# 		result.test13 = True
					#
					# # if True:
					# if not result.test14:
					# 	if test_fourteen.search(line):
					# 		result.test14 = True
					#
					# # if True:
					# if not result.test15:
					# 	if test_fifteen.search(line):
					# 		result.test15 = True
					#
					# # if True:
					# if not result.test16:
					# 	if test_sixteen.search(line):
					# 		result.test16 = True
					#
					# # if True:
					# if not result.test17:
					# 	if test_seventeen.search(line):
					# 		# fileTestOnec.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test17 = True
					#
					# # if True:
					# if not result.test18:
					# 	if test_eigteen.search(line):
					# 		# fileTestTwoc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test18 = True
					#
					# # if True:
					# if not result.test19:
					# 	if test_nineteen.search(line):
					# 		# fileTestThreec.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test19 = True
					#
					# # if True:
					# if not result.test20:
					# 	if test_twenty.search(line):
					# 		# fileTestFourc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test20 = True
					#
					# # if True:
					# if not result.test21:
					# 	if test_twentyone.search(line):
					# 		# fileTestFivec.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test21 = True
					#
					# # if True:
					# if not result.test22:
					# 	if test_twentytwo.search(line):
					# 		# fileTestSixc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test22 = True
					#
					# # if True:
					# if not result.test23:
					# 	if test_twentrythree.search(line):
					# 		# fileTestSevenc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test23 = True
					#
					# # if True:
					# if not result.test24:
					# 	if test_twentyfour.search(line):
					# 		# fileTestEightc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
					# 		result.test24 = True
					#
					# file_one.close()
#######################
					# for i,line in enumerate(context_one):
					# #for i,line in enumerate(file_one):
					# 	#print(line)
					# #for line in content:
					# 	# print("===============")
					# 	# print(line)
					# 	# print("===============")
					# 	line=line.lower()
					# 	line.strip()
					# 	#if(True):
					#
					# 	context = getContext(i, context_one)
					# other = Model.getOtherApp(self, result)
					# checkTest1=(other.subIAP)# or other.consummableIAP)
					# # checkTest2=(other.subIAP)# or other.consummableIAP)
					# # checkTest3=(other.subIAP)# or other.consummableIAP)
# # 						if not (result.consummableIAP):# and (not "api" in checking) and (not "google" in checking) and (not "IInAppBillingService" in checking)):
# # 							if consummablePattern.search(line):
# # 								result.consummableIAP = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# # 									if (other.consummableIAP == True):
# # 										fileCon.write(
# # 											result.Title + "=(good consummableIAP)=" + line + " in " + checking + "\n")
# # 									else:
# # 										fileCon.write(
# # 											result.Title + "=(bad consummableIAP)=" + line + " in " + checking + "\n")
# #
# #
# # 						if not result.subIAP:
# # 						#if True:
# # 							if subPattern.search(line):
# # 							#	fileIAP.write(result.Title+"=(subscription)="+line+" in" +checking+"\n")
# # 								result.subIAP = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# #
# # 									#print("yes!")
# # 									if (other.subIAP == True):
# # 										fileIAP.write(
# # 											result.Title + "=(good subIAP)=" + line + " in " + checking + "\n")
# # 									else:
# # 										fileIAP.write(
# # 											result.Title + "=(bad subIAP)=" + line + " in " + checking + "\n")
# #
# # 						if not result.permanentIAP:
# # 							if permanentPattern.search(line):
# # 								# print(game,"=",line,"in ",checking)
# # 							#	filePerm.write(result.Title+ "=(permanent)="+ line+ " in "+ checking + "\n")
# # 								result.permanentIAP = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# # 									if (other.permanentIAP == True):
# # 										filePerm.write(
# # 											result.Title + "=(good permanentIAP)=" + line + " in " + checking + "\n")
# # 									else:
# # 										filePerm.write(
# # 											result.Title + "=(bad permanentIAP)=" + line + " in " + checking + "\n")
# #
# # 						if not (result.rewardedAds):
# # 							if rewardedPattern.search(line):
# # 							#	fileRew.write(result.Title+"=(rewarded)="+line+" in "+checking+"\n")
# # 								result.rewardedAds = True
# # 							if (filing == True):
# # 								other = Model.getOtherApp(self, result)
# # 								if (other.rewardedAds == True):
# # 									fileRew.write(
# # 										result.Title + "=(good rewardedAds)=" + line + " in " + checking + "\n")
# # 								else:
# # 									fileRew.write(
# # 										result.Title + "=(bad rewardedAds)=" + line + " in " + checking + "\n")
# #
# # 						if not result.interstitialAds:
# # 							if InterPattern.search(line):
# # 								result.interstitialAds = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# # 									if (other.interstitialAds == True):
# # 										fileInterOne.write(
# # 											result.Title + "=(good interstitialAds)=" + line + " in " + checking + "\n")
# # 									else:
# # 										fileInterOne.write(
# # 											result.Title + "=(bad interstitialAds)=" + line + " in " + checking + "\n")
# #
# # 						if not result.removeAds:
# # 							if removeAdPattern.search(line):
# # 								result.removeAds = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# # 									if (other.removeAds == True):
# # 										fileRemoveAds.write(
# # 											result.Title + "=(good removeAds)=" + line + " in " + checking + "\n")
# # 									else:
# # 										fileRemoveAds.write(
# # 											result.Title + "=(bad removeAds)=" + line + " in " + checking + "\n")
# #
# # 						#if(False):
# # 						if not result.offerwall:
# # 							for a in offerwall_stuff:
# # 								#print(str(a))
# # 								if a.search(line):
# # 									result.offerwall = True
# # 									break
# # 							#if offerwallPattern.search(line):
# # 							#	fileInterTwo.write(result.Title+ "=(offerwall)="+ line+ " in "+ checking + "\n")
# # 								result.offerwall = True
# #
# # 						#if(False):
# # 						if not result.nativeAds:
# # 							if nativeAdsPattern.search(line) or nativeAdsPattern3.search(line):
# # 								#fileADS.write(result.Title+ "=(native)="+ line+ " in "+ checking + "\n")
# # 								result.nativeAds = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# # 									if (other.nativeAds == True):
# # 										fileTestOne.write(
# # 											result.Title + "=(good nativeAds)=" + line + " in " + checking + "\n")
# # 									else:
# # 										fileTestOne.write(
# # 											result.Title + "=(bad nativeAds)=" + line + " in " + checking + "\n")
# #
# # 						#if(False):
# # 						if not result.leaderboard:
# # 							if leaderboardPattern.search(line):
# # 								result.leaderboard = True
# # 								if (filing == True):
# # 									other = Model.getOtherApp(self, result)
# # 									if (other.leaderboard == True):
# # 										fileTestOne.write(
# # 											result.Title + "=(good leaderboard)=" + line + " in " + checking + "\n")
# # 									else:
# # 										fileTestOne.write(
# # 											result.Title + "=(bad leaderboard)=" + line + " in " + checking + "\n")
# # 								fileLeader.write(result.Title + "=(leader)=" + line + " in " + checking + "\n")
# # # ####################################
# 						#if True:
# 					#if notification_perm:
# 					#if True:
# 						#TODO: fix this and redo the test >.>
# 						#if True:
# 					#if not filer=="GoogleApiAvailability.java":
					#if True:
					if (not result.test1) or filery:
						if test_one.search(line):
							result.test1 = True
							if (filing == True):
								#other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									#fileTestOne.write(result.Title + context + " in " + checking + "\n")
									fileTestOne.write(result.Title + " in " + checking + "\n")
								else:
									fileTestOneBad.write(result.Title + " in " + checking + "\n")

					if (not result.test2) or filery:
						if test_two.search(line):
							result.test2 = True
							if (filing == True):
								#other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestTwo.write(result.Title + " in " + checking + "\n")
								else:
									fileTestTwoBad.write(result.Title + " in " + checking + "\n")

								#fileTestTwo.write(result.Title + "=test2=" + line + " in " + checking + "\n")

					if (not result.test3) or filery:
						if test_three.search(line):
							result.test3 = True
							if (filing == True):
								#other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestThree.write(result.Title + " in " + checking + "\n")
								else:
									fileTestThreeBad.write(result.Title + " in " + checking + "\n")
								#fileTestThree.write(result.Title + "=test3=" + line + " in " + checking + "\n")

					if (not result.test4) or filery:
						if test_four.search(line):
							result.test4 = True
							if (filing == True):
								#other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestFour.write(result.Title + " in " + checking + "\n")
								else:
									fileTestFourBad.write(result.Title + " in " + checking + "\n")
								#fileTestFour.write(result.Title + "=test4=" + line + " in " + checking + "\n")

					if (not result.test5) or filery:
						if test_five.search(line):
							result.test5 = True
							if (filing == True):
								#other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestFive.write(result.Title + " in " + checking + "\n")
								else:
									fileTestFiveBad.write(result.Title + " in " + checking + "\n")
								#fileTestFive.write(result.Title + "=test5=" + line + " in " + checking + "\n")

					if (not result.test6) or filery:
						if test_six.search(line):
							result.test6 = True
							if (filing == True):
								#other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestSix.write(result.Title + " in " + checking + "\n")
								else:
									fileTestSixBad.write(result.Title + " in " + checking + "\n")
								#fileTestSix.write(result.Title + "=test6=" + line + " in " + checking + "\n")

					if (not result.test7) or filery:
						if test_seven.search(line):
							result.test7 = True
							if (filing == True):
							#	other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestSeven.write(result.Title + " in " + checking + "\n")
								else:
									fileTestSevenBad.write(result.Title + " in " + checking + "\n")
									#fileTestSeven.write(result.Title + "=test7=" + line + " in " + checking + "\n")

					if (not result.test8) or filery:
						if test_eight.search(line):
							result.test8 = True
							if (filing == True):
							#	other = Model.getOtherApp(self, result)
								if (checkTest1==True):
									fileTestEight.write(result.Title + " in " + checking + "\n")
								else:
									fileTestEightBad.write(result.Title + " in " + checking + "\n")

				# 	if (not result.test9) or filery:
				# 		if test_nine.search(line):
				# 			result.test9 = True
				# 			if (filing == True):
				# 			#	other = Model.getOtherApp(self, result)
				# 				if(checkTest2==True):
				# 				#if (other.push_notification == True):
				# 					fileTestOneb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestOnebBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestOneb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test10) or filery:
				# 		if test_ten.search(line):
				# 			result.test10 = True
				# 			if (filing == True):
				# 			#	other = Model.getOtherApp(self, result)
				# 				#if (other.push_notification == True):
				# 				if (checkTest2 == True):
				# 					fileTestTwob.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestTwobBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestTwob.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test11) or filery:
				# 		if test_eleven.search(line):
				# 			result.test11 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestThreeb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestThreebBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestThreeb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test12) or filery:
				# 		if test_twelve.search(line):
				# 			result.test12 = True
				# 			if (filing == True):
				# 			#	other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestFourb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestFourbBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestFourb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test13) or filery:
				# 		if test_thirteen.search(line):
				# 			result.test13 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestFiveb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestFivebBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestFiveb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test14) or filery:
				# 		if test_fourteen.search(line):
				# 			result.test14 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				#if (checkTest2 == True):
				# 				if (checkTest2 == True):
				# 					fileTestSixb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestSixbBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestSixb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test15) or filery:
				# 		if test_fifteen.search(line):
				# 			result.test15 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestSevenb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestSevenbBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestSevenb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test16) or filery:
				# 		if test_sixteen.search(line):
				# 			result.test16 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestEightb.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestEightbBad.write(result.Title + " in " + checking + "\n")
				# 				#fileTestEightb.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				#
				# 	if (not result.test17) or filery:
				# 		if test_seventeen.search(line):
				# 			#fileTestOnec.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.push_notification = True
				# 			if (filing == True):
				# #				context = getContext(enumerate, context_one)
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest3 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestOnec.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestOnecBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test18) or filery:
				# 		if test_eigteen.search(line):
				# 			#fileTestTwoc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.push_notification = True
				# 			if (filing == True):
				# 		#		context = getContext(enumerate, context_one)
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest3 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestTwoc.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestTwocBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test19) or filery:
				# 		if test_nineteen.search(line):
				# 			#fileTestThreec.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.push_notification = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest3 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestThreec.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestThreecBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test20) or filery:
				# 		if test_twenty.search(line):
				# 			#fileTestFourc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.test20 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestFourc.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestFourcBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test21) or filery:
				# 		if test_twentyone.search(line):
				# 			#fileTestFivec.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.test21 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest2 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestFivec.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestFivecBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test22) or filery:
				# 		if test_twentytwo.search(line):
				# 			#fileTestSixc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.test22 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest3 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestSixc.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestSixcBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test23) or filery:
				# 		if test_twentrythree.search(line):
				# 			#fileTestSevenc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.test23 = True
				# 			if(filing==True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest3 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestSevenc.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestSevencBad.write(result.Title + " in " + checking + "\n")
				#
				# 	if (not result.test24) or filery:
				# 		if test_twentyfour.search(line):
				# 			#fileTestEightc.write(result.Title + "=test7=" + line + " in " + checking + "\n")
				# 			result.test24 = True
				# 			if (filing == True):
				# 				#other = Model.getOtherApp(self, result)
				# 				if (checkTest3 == True):
				# 				#if (other.push_notification == True):
				# 					fileTestEightc.write(result.Title + " in " + checking + "\n")
				# 				else:
				# 					fileTestEightcBad.write(result.Title + " in " + checking + "\n")

					file_one.close()

				file_done = file_done + 1
				#print(file_done)

				global threshold
				curr=(file_done/file_count)*100
				if(curr>threshold):
					print(str(threshold)+"%",file_done)
					threshold=threshold+1
				#print(str(round(file_done/file_count,1))+"\n")
				#if(round(file_done/file_count,1)%0.1==0):
				#	print("go!")

		#print("PRE test")
		if filery==True:
			fileRew.close()
			fileCon.close()
			filePerm.close()
			fileInterOne.close()
			fileInterTwo.close()
			fileIAP.close()

			# fileTestOne.write("\n")
			# fileTestTwo.write("\n")
			# fileTestThree.write("\n")
			# fileTestFour.write("\n")
			# fileTestFive.write("\n")
			# fileTestSix.write("\n")
			# fileTestSeven.write("\n")
			# fileTestEight.write("\n")

			fileTestOne.close()
			fileTestTwo.close()
			fileTestThree.close()
			fileTestFour.close()
			fileTestFive.close()
			fileTestSix.close()
			fileTestSeven.close()
			fileTestEight.close()
			fileTestOneBad.close()
			fileTestTwoBad.close()
			fileTestThreeBad.close()
			fileTestFourBad.close()
			fileTestFiveBad.close()
			fileTestSixBad.close()
			fileTestSevenBad.close()
			fileTestEightBad.close()

			# fileTestOneb.write("\n")
			# fileTestTwob.write("\n")
			# fileTestThreeb.write("\n")
			# fileTestFourb.write("\n")
			# fileTestFiveb.write("\n")
			# fileTestSixb.write("\n")
			# fileTestSevenb.write("\n")
			# fileTestEightb.write("\n")

			fileTestOneb.close()
			fileTestTwob.close()
			fileTestThreeb.close()
			fileTestFourb.close()
			fileTestFiveb.close()
			fileTestSixb.close()
			fileTestSevenb.close()
			fileTestEightb.close()
			fileTestOnebBad.close()
			fileTestTwobBad.close()
			fileTestThreebBad.close()
			fileTestFourbBad.close()
			fileTestFivebBad.close()
			fileTestSixbBad.close()
			fileTestSevenbBad.close()
			fileTestEightbBad.close()

			# fileTestOnec.write("\n")
			# fileTestTwoc.write("\n")
			# fileTestThreec.write("\n")
			# fileTestFourc.write("\n")
			# fileTestFivec.write("\n")
			# fileTestSixc.write("\n")
			# fileTestSevenc.write("\n")
			# fileTestEightc.write("\n")

			fileTestOnec.close()
			fileTestTwoc.close()
			fileTestThreec.close()
			fileTestFourc.close()
			fileTestFivec.close()
			fileTestSixc.close()
			fileTestSevenc.close()
			fileTestEightc.close()
			fileTestOnecBad.close()
			fileTestTwocBad.close()
			fileTestThreecBad.close()
			fileTestFourcBad.close()
			fileTestFivecBad.close()
			fileTestSixcBad.close()
			fileTestSevencBad.close()
			fileTestEightcBad.close()

		#print(result.id)
		# file_done=file_done+1
		#global threshold
		# curr=(file_done/file_count)*100
		# if(curr>threshold):
		# 	print(str(threshold) + "%")
		# 	threshold = threshold + 1
		return result

	#analyse single app with androguard
	# deprecated, probably doesn't work anymore
	# def analyse_single_androguard(Apk_file,linux):
	# 	global mode
	# 	mode = "androguard"
	# 	outFile = open("flagged.txt","w",encoding="utf-8")
	# 	result = application.application()
	# 	#result.name = "com.zplay.willhero"
	# 	result.name=Apk_file
	# 	GetStoreInfo(result)
	# 	print("start",result.name)
	# 	a, d, dx = test(Apk_file)
	# 	print("=========================")
	# 	result.id=a.get_package()
	# 	GetStoreInfo(result)
	#
	# 	fileIAP=open("androiap.txt","a",encoding="utf-8")
	# 	#fileADS=open("androads.txt","a",encoding="utf-8")
	#
	# 	#testing=open("androtest.txt","a",encoding="utf-8")
	# 	#testing.write("yes!")
	# 	#testing.close()
	#
	# 	consummablePattern = ".*onsumePurchas.*"
	# 	earnedPattern=".*EarnedRewar.*"
	# 	#interstitialPattern=".*nterstitialA.*"
	# 	subscribePattern=".*ubscriptio.*"
	# 	subscribePattern=".*sAutoRenewin.*"
	# 	interstitialPattern=".*nAdShowedFullScreenConten.*"
	# 	#interstitialPattern = "OnAdShowedFullScreenContent"
	# 	offerwallPattern=".*offerwal.*"
	# 	permanentIAP="getPurchaseState"
	# 	nativeAdPattern=".*annerA.*"
	# 	nativeAdPattern="AdSize"
	# 	notificationPattern="createNotificationChannel"
	#
	# 	# for meth in dx.find_methods(methodname=notificationPattern):
	# 	# 	result.push_notification=True
	# 	# 	fileIAP.write(result.Title + "~~(consummable)~~" + meth.get_method().name + " ~~class~~" + meth.class_name + "\n")
	# 	# 	break
	#
	# 	#if(dx.find_methods(methodname=consummablePattern)):
	# 	for meth in dx.find_methods(methodname=consummablePattern):
	# 		result.consummableIAP = True
	# 	#	print("consu")
	# 	#	fileIAP.write(result.Title + "~~(consummable)~~" + meth.get_method().name +" ~~class~~"+meth.class_name+"\n")
	# 		break
	#
	# 	for meth in dx.find_methods(methodname=nativeAdPattern):
	# 	#	print("native")
	# 		result.nativeAds = True
	# 	#	fileADS.write(result.Title + "~~(native)~~" + meth.get_method().name+" ~~class~~"+ meth.class_name+"\n")
	# 		break
	#
	# 	for meth in dx.find_methods(methodname=earnedPattern):
	# 		#print("earned")
	# 	#	fileADS.write(result.Title + "~~(rewarded)~~" + meth.get_method().name+" ~~class~~"+ meth.class_name+"\n")
	# 		result.rewardedAds=True
	# 		break
	#
	# 	for meth in dx.find_methods(methodname=interstitialPattern):
	# 		#print("inter")
	# 		result.interstitialAds=True
	# 		#fileADS.write(result.Title + "~~(interstitial)~~" + meth.get_method().name+" ~~class~~"+ meth.class_name+"\n")
	# 		break
	#
	# 	for meth in dx.find_methods(methodname=subscribePattern):
	# 	#	print("sub")
	# 		result.subIAP=True
	# 	#	fileIAP.write(result.Title + "~~(subscribe)~~" + meth.get_method().name+" ~~class~~"+ meth.class_name+"\n")
	# 		#print("detected")
	# 		break
	#
	# 	for meth in dx.find_methods(methodname=offerwallPattern):
	# 	#	print("offer")
	# 		result.offerwall=True
	# 	#fileADS.write(result.Title + "~~(offerwall)~~" + meth.get_method().name+" ~~class~~"+ meth.class_name+"\n")
	# 		break
	#
	# 	for meth in dx.find_methods(methodname=permanentIAP):
	# 		#print("perm")
	# 		result.permanentIAP=True
	# 	#	fileIAP.write(result.Title + "~~(permanent)~~" + meth.get_method().name+" ~~class~~"+ meth.class_name+"\n")
	# 		break
	# 	#fileIAP.write(result.Title + "=ugh=" + meth + " class=" + meth.class_name)
	# 	#fileADS.close()
	# 	#fileIAP.close()
	# 	print("end", result.name)
	# 	return result



	def analyse_all(self,folder):
		"""
		analyse all apps in the folder
		:param folder: folder containing the applications code folder
		:return: nothing
		"""
		for appsDir in os.listdir(folder):
			#applicationers=application.application()
			path=folder+appsDir
			appli= Model.analyse_single(path, 0)
			self.list_applis.append(appli)

	def analyse_allT(self, folder, linux):
		"""
		analyse all apps in the folder
		:param folder: folder containing the applications code folder
		:return: nothing
		"""
		print("analyse_allT")
		tasks=[]
		global jadx
		if(linux):
			if(jadx):
				decExtension = "/sources"
				#decExtension = "/exp"
				#unpackExtension="/resources"
			else:
				decExtension = "/decompiled"
		else:
			if(jadx):
				decExtension = "\\sources"
				#decExtension = "\\exp"
			else:
				decExtension = "\\decompiled"
		global file_count
		for dirs in os.listdir(folder):
			tempo=0
			for (heh, hoh, files) in os.walk((folder + dirs + decExtension), topdown=True):
				tempo=tempo+1
				file_count = file_count + len(files)
			print("counting done",file_count,dirs,folder,"(",tempo,")")

		ts=time.time()
		with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
			for gFolder in os.listdir(folder):
				path=folder+gFolder
				tasks.append(executor.submit(Model.analyse_single, self,path,linux))
			for future in as_completed(tasks):
				self.list_applis.append(future.result())
		ts_end=time.time()
		time_total=ts_end-ts
		print("time start:",ts)
		print("time done:",ts_end)
		print("time taken to look at it all:",time_total)
		self.list_applis.sort(key=lambda x:x.Title)


	def separate(self,folder):
		"""
		separate the apps containing an aspect from the apps not containing the same aspect
		results are written in the "separated" folder
		:return: nothing
		"""
		reals_three = Truths_final.Truth_final()
		print("sep")
		reals_three.loadTruth_final("datasets/donnes_vrai_recent_secC.xlsx")
		#reals_three.loadTruth_final("datasets/donne_vrai_phase_fin_whatC.xlsx")
		final_Truth = reals_three.getTruths_final()
		a=0
		delme=open("separated/delme.txt","a",encoding="utf-8")
		included = open("separated/include.txt","w",encoding="utf-8")
		excluded = open("separated/exclude.txt","w",encoding="utf-8")
		for dirs in final_Truth:
			app=final_Truth[dirs]
			if dirs in self.translation_name_to_id:
				app.id=self.translation_name_to_id[dirs]

				if (app.push_notification):
					included.write(app.id + "\n")
				else:
					excluded.write(app.id + "\n")
				a=a+1
		delme.close()
		included.close()
		excluded.close()
		print("number treated=",a)

	#deprecated
	def separate_ori(self,folder,linux):
		if (jadx):
			if (linux):
				manExtension = "/resources/AndroidManifest.xml"
			else:
				manExtension = "\\resources\\AndroidManifest.xml"
		else:
			if (linux):
				manExtension = "/unpacked/AndroidManifest.xml"
			else:
				manExtension = "\\unpacked\\AndroidManifest.xml"
		a=0
		delme=open("separated/delme.txt","a",encoding="utf-8")
		included = open("separated/include.txt","a",encoding="utf-8")
		excluded = open("separated/exclude.txt","a",encoding="utf-8")
		for dirs in os.listdir(folder):
			exist=False
			app = application.application()
			app.name=folder
			path=folder+dirs
			#print(dirs)
			manifest = open(path + manExtension,encoding="cp437")
			man = manifest.read()
			position_first = man.find("package=\"") + 9
			position_last = man.find("\"", position_first)
			manifest.close()
			app.id = man[position_first:position_last]
			#print("\n",app.id,"is being treated(",a,")",end=' ')
			GetStoreInfo(app)
			if (app.Title in self.list_Truths):
				#print(app.Title,"supposed to exist(",a,")")
				exist = True
			elif (app.id in self.translation):
				#print("in translation")
				app.Title = self.translation[app.id]
				if (app.Title in self.list_Truths):
					#print(app.Title,"was translated(",a,")")
					exist=True
				else:
					print(app.Title,"was never found :(  (",a,")")

			if(exist):
				print(app.Title,"exist!")
				res = self.list_Truths[app.Title]
				inf=app.id+","+str(res.version)+"\n"
				delme.write(inf)

				if(res.removeAds):
					included.write(dirs+"\n")
					#included.write(app.Title + "\n")
				else:
					excluded.write(dirs+"\n")
					#excluded.write(app.Title + "\n")

			else:
				#a=0
				print(app.Title,"doesn't exist, somehow")
			a=a+1
			exist=False
		delme.close()
		included.close()
		excluded.close()
		print("number treated=",a)


	#deprecated
	@loguru_disable("androguard")
	def analyse_allTAndro(self, folder, linux):
	#def analyse_allT(self, folder, linux,truth):
		#reals = Truths.Truth()
		#list_Truths = reals.getTruths()
		tasks=[]

		with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
			for gFolder in os.listdir(folder):
				#print(gFolder)
				path=folder+gFolder
				#tasks.append(executor.submit(checkOneMT,gFolder))
				tasks.append(executor.submit(Model.analyse_single_androguard, path,linux))
			for future in as_completed(tasks):
				#print("done")
				self.list_applis.append(future.result())
				#print(self.listfuture.result())