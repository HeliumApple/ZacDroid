import tkinter
from tkinter import ttk, Frame, Button, filedialog, VERTICAL, RIGHT, Y, LEFT, BOTH
from tkinter.ttk import Scrollbar
#REMOVE TK
from contextlib import contextmanager

import loguru

from Model import Model, test2, test3
from sections import general
from sections.IAP import IAP
from sections.ads import ads
from sections.general import general
from sections.Structure import Structure
from sections.stats.StatIAP import StatIAP
from sections.social import Social
from sections.term_test import test
from sections.term_test2 import test2
from sections.term_test3 import test3

@contextmanager
def loguru_disable(name):
    loguru.logger.disable(name)
    try:
        yield
    finally:
        loguru.logger.enable(name)

@loguru_disable("androguard")
class View(ttk.Frame):

	folders=[]
	folder=""
	truth=""
	data=[]
	tabs=[]
	canvases={}


	def __init__(self,parent):

		def SelectTruthFolder():

			#f=open("result_notif_manyfilter_cperm.json")
			#f = open("result_notif_manyfilter_cperm_removeblankforscreenshot.json")
			#f = open("result_PurchasesNoSub.json")
			f = open("result_halp.json")
			print("################################\n##################\n###########")
			self.controller.importJSON(f.read())
			#ShowAll()


			# filename = filedialog.askopenfilename()
			# print("filename is:",filename)
			# ##TODO: find a better way than this mess
			# #filename=filename.replace("/","\\")
			# filename = filename.replace("\\", "O")
			# #foldername=foldername+"\\"
			# self.truth=filename

		@loguru_disable("androguard")
		def Analyse():
			self.folder="emptydelme/"
			if self.controller:

				for folder in self.folders:
					self.controller.analyse(folder)

				#self.controller.analyse(self.folder)
				#f = open("result.json")
				#fileJSON=f.read()
				#self.controller.importJSON(fileJSON)
				#data=self.controller.getApps()
				# #showAds(a)
				# print(data)
				# ShowAll()


		def SelectAppFolder():
			foldername = filedialog.askdirectory()
			#print(foldername)
			##TODO: find a better way than this mess
			foldername=foldername.replace("/","\\")
			foldername=foldername+"\\"
			self.folders.append(foldername)
			self.folder=foldername
			#print(self.folders)

		def showIAP(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_iap = self.controller.getIAP()
			self.tabs[0].update(application_data_iap)
			IAP.addApp(self.tabs[0])

		def showAds(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_ads = self.controller.getAds()
			#print(application_data_ads)
			self.tabs[1].update(application_data_ads)
			#print(tab2)
			ads.addApp(self.tabs[1])

		def showGen(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_gen = self.controller.getGen()
			self.tabs[2].update(application_data_gen)
			general.addApp(self.tabs[2])

		def showStruct(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_struct = self.controller.getStruct()
			self.tabs[3].update(application_data_struct)
			Structure.addApp(self.tabs[3])

		def showSocial(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_social = self.controller.getSocial()
			self.tabs[4].update(application_data_social)
			Social.addApp(self.tabs[4])

		def showTest(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_test = self.controller.getTest()
			self.tabs[5].update(application_data_test)
			test.addApp(self.tabs[5])

		def showTest2(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_test2 = self.controller.getTest2()
			self.tabs[6].update(application_data_test2)
			test2.addApp(self.tabs[6])

		def showTest3(tab_frame):
			#self.configure()
			if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
				return
			application_data_test3 = self.controller.getTest3()
			self.tabs[7].update(application_data_test3)
			test2.addApp(self.tabs[7])


		# def showTest3(tab_frame):
		# 	self.configure()
		# 	if hasattr(tab_frame, 'content_loaded') and tab_frame.content_loaded:
		# 		return
		# 	application_data_test3 = self.controller.getTest3()
		# 	self.tabs[7].update(application_data_test3)
		# 	test3.addApp(self.tabs[7], tab8)

		def clear_tab(tab_frame):
			#print("clear")
			#for a in self.tabs:
			# for widget in tab_frame.winfo_children():
			# 	#print("widget:",widget)
			# 	widget.destroy()
			#tab_frame.content_loaded=False
			tab_index = self.tabControl.index(tab_frame)
			tab_obj=self.tabs[tab_index]
			tab_obj.reset()
			# self.tabs[0]=IAP(tab1)
			# self.tabs[1]=ads(tab2)
			# print("clearing ads")
			# self.tabs[2]=general(tab3)
			# self.tabs[3]=Structure(tab4)
			# self.tabs[4]=Social(tab5)
			# self.tabs[5]=test(tab6)
			# self.tabs[6]=test2(tab7)
			# self.tabs[7]=test3(tab8)
			#print(self.tabs)

		def on_tab_change(event):
			#tab_frame.content_loaded = False
			# self.tabs[0] = IAP(tab1)
			# self.tabs[1] = ads(tab2)
			# print("clearing ads")
			# self.tabs[2] = general(tab3)
			# self.tabs[3] = Structure(tab4)
			# self.tabs[4] = Social(tab5)
			# self.tabs[5] = test(tab6)
			# self.tabs[6] = test2(tab7)
			# self.tabs[7] = test3(tab8)
			selected_tab=event.widget.select()
			print("selected:",selected_tab)
			for tab in [tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8]:
				if str(tab)!=selected_tab:
					#print("clearing tab:",tab)
					clear_tab(tab)

			if selected_tab == str(tab1):
			#	print("Showing tab1")
				showIAP(tab1)
			elif selected_tab == str(tab2):
			#	print("Showing tab2")
				showAds(tab2)
			elif selected_tab == str(tab3):
				showGen(tab3)
			elif selected_tab == str(tab4):
			#	print("Showing tab4")
				showStruct(tab4)
			elif selected_tab == str(tab5):
			#	print("Showing tab5")
				showSocial(tab5)
			elif selected_tab == str(tab6):
			#	print("Showing tab6")
				showTest(tab6)
			elif selected_tab == str(tab7):
			#	print("Showing tab7")
				showTest2(tab7)
			elif selected_tab == str(tab8):
			#	print("Showing tab8")
				showTest3(tab8)

		def ShowAll():
			if self.controller:
				self.configure()
				application_data_iap = self.controller.getIAP()
				self.tabs[0].update(application_data_iap)
				IAP.addApp(self.tabs[0],tab1)

				application_data_ads=self.controller.getAds()
				self.tabs[1].update(application_data_ads)
				ads.addApp(self.tabs[1],tab2)

				application_data_gen = self.controller.getGen()
				self.tabs[2].update(application_data_gen)
				general.addApp(self.tabs[2],tab3)

				application_data_struct = self.controller.getStruct()
				self.tabs[3].update(application_data_struct)
				Structure.addApp(self.tabs[3],tab4)

				application_data_social=self.controller.getSocial()
				self.tabs[4].update(application_data_social)
				Social.addApp(self.tabs[4],tab5)

				application_data_test=self.controller.getTest()
				self.tabs[5].update(application_data_test)
				test.addApp(self.tabs[5],tab6)

				application_data_test2 = self.controller.getTest2()
				self.tabs[6].update(application_data_test2)
				test2.addApp(self.tabs[6], tab6)

				application_data_test3 = self.controller.getTest3()
				self.tabs[7].update(application_data_test3)
				test3.addApp(self.tabs[7], tab6)



		super().__init__(parent)

		Result_frame = Frame(parent)
		Button_frame = Frame(parent,width=100,height=100)

		self.tabControl=ttk.Notebook(parent)
		self.scrollbar = ttk.Scrollbar(self,orient=VERTICAL)
		self.scrollbar.pack(side=RIGHT, fill=Y)

		tab1 = ttk.Frame(self.tabControl)
		tab2 = ttk.Frame(self.tabControl)
		tab3 = ttk.Frame(self.tabControl)
		tab4 = ttk.Frame(self.tabControl)
		tab5 = ttk.Frame(self.tabControl)
		tab6 = ttk.Frame(self.tabControl)
		tab7 = ttk.Frame(self.tabControl)
		tab8 = ttk.Frame(self.tabControl)


		self.tabControl.add(tab1, text='microtransactions')
		self.tabControl.add(tab2, text='publicités')
		self.tabControl.add(tab3, text='informations general')
		self.tabControl.add(tab4, text='Structure')
		self.tabControl.add(tab5, text="Social")
		self.tabControl.add(tab6,text="tests 1")
		self.tabControl.add(tab7,text="tests 2")
		self.tabControl.add(tab8,text="tests 3")
		self.tabControl.pack(expand=1, fill="both")

		self.tabs.append(IAP(tab1))
		self.tabs.append(ads(tab2))
		#("Why, though?")
		self.tabs.append(general(tab3))
		self.tabs.append(Structure(tab4))
		self.tabs.append(Social(tab5))
		self.tabs.append(test(tab6))
		self.tabs.append(test2(tab7))
		self.tabs.append(test3(tab8))

		select_folder = Button(Button_frame,text="selection",command=SelectAppFolder)
		Analyse_button = Button(Button_frame,text="analyse",command=Analyse)
		select_truth = Button(Button_frame,text="importation",command=SelectTruthFolder)
		scrollbar=Scrollbar(self,orient=VERTICAL)

		Analyse_button.pack()
		select_folder.pack()
		select_truth.pack()
		scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)

		Result_frame.pack(padx=1, pady=1)
		Button_frame.pack(padx=10,pady=10)

		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab1: showIAP())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab2: showAds())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab3: showGen())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab1: showStruct())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab2: showSocial())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab3: showTest())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab1: showTest2())
		# parent.bind("<<NotebookTabChanged>>", lambda event, tab=tab2: showTest3())

		#parent.bind("<<NotebookTabChanged>>", on_tab_change)
		self.tabControl.bind("<<NotebookTabChanged>>", on_tab_change)
		self.controller = None

	def set_controller(self,controller):
		self.controller = controller