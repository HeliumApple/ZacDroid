from contextlib import contextmanager

import loguru

#from ModelLinux import ModelLinux, loguru_disable

@contextmanager
def loguru_disable(name):
    loguru.logger.disable(name)
    try:
        yield
    finally:
        loguru.logger.enable(name)

@loguru_disable("androguard")
class Controller:

	@contextmanager
	def loguru_disable(name):
		loguru.logger.disable(name)
		try:
			yield
		finally:
			loguru.logger.enable(name)
	def __init__(self,model,view):
		self.model=model
		self.view=view

	@loguru_disable("androguard")
	def analyse(self, folder):
		self.model.analyse_allT(folder, True)
		#self.model.separate(folder,False)

	def analyse_cli(self,folder):
		self.model.analyse_allT(folder,True)
		#TODO: improve
		f=open("result.json","a")
		res=self.model.get_data_export()
		f.write(res)
		f.close()

	def getJSON(self):
		return(self.model.get_data_export())

	def importJSON(self,json):
		return(self.model.get_data_import(json))

	def getApps(self):
		return(self.model.getApplis())
		#print(self.model.getApplis())

	def getGen(self):
		return(self.model.getGeneral())

	def getIAP(self):
		return(self.model.getIAP())

	def getAds(self):
		return(self.model.getAds())

	def getTest(self):
		return(self.model.getTest())

	def getTest2(self):
		return(self.model.getTest2())

	def getTest3(self):
		return(self.model.getTest3())

	def getStruct(self):
		return(self.model.getStructure())

	def getSocial(self):
		return(self.model.getSocial())

	# def getIAPStat(self):
	# 	return(self.model.getIAPStat())
	#
	# def getSocialStat(self):
	# 	return(self.model.getSocialStat())
	#
	# def getAdsStat(self):
	# 	return(self.model.getAdsStat())
	#
	# def getStructureStat(self):
	# 	return(self.model.getStructureStat())


