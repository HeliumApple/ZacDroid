import copy
from pickle import FALSE
from tkinter import ttk, Canvas, LEFT, BOTH, VERTICAL, RIGHT, Y
from tkinter.ttk import Scrollbar



class ads(ttk.Frame):
	application_data = [[], [], [], [],[]]
	grids = [[], [], [], [], [],[]]

	falseP = 0
	trueP = 0
	falseN = 0
	trueN = 0

	windower = []


	def rewardedStat(self):
		precisionData=[-1.0,-1.0,-1.0,-1.0]
		rappelData=[-1.0,-1.0,-1.0,-1.0]
		stuff=[]
		included = open("separated/include_more.txt","w",encoding="utf-8")
		excluded = open("separated/exclude_more.txt","w",encoding="utf-8")
		for a in range(1,len(self.application_data)):
			falseP = 0
			trueP = 0
			falseN = 0
			trueN = 0
			s = self.application_data[a]
			print(self.application_data[0])
			for num,d in enumerate(s):
				if(d[0]==False and d[1]=='green'):
					trueN=trueN+1
				elif(d[0]==False and d[1]=='red'):
					falseN=falseN+1
				elif(d[0]==True and d[1]=='green'):
					trueP=trueP+1
				elif(d[0]==True and d[1]=='red'):
					falseP=falseP+1

			self.falseN=self.falseN+falseN
			self.falseP=self.falseP+falseP
			self.trueP=self.trueP+trueP
			self.trueN=self.trueN+trueN
			if(trueP+falseP==0):
				precision=-2
			else:
				precision=trueP/(trueP+falseP)

			if(trueP+falseN==0):
				rappel=-2
			else:
				rappel=trueP/(trueP+falseN)
			precisionData[a-1]=round(precision,3)
			rappelData[a-1]=round(rappel,3)
			tempo=[trueN,falseN,trueP,falseP]
			stuff.append(tempo)
			#print("trueP=", trueP, "falseP=", falseP, "trueN=", trueN, "falseN=", falseN)
		excluded.close()
		included.close()
		print("done calculating")
		return precisionData,rappelData,stuff

	def __init__(self,parent):
		super().__init__()

		self.canvas=Canvas(parent)
		self.parent=parent
		self.build_ui()

	def build_ui(self):
		self.canvas = Canvas(self.parent)
		categories = ["rewarded", "Interstitial", "offerwall", "native"]
		self.windower = []
		scrollbar = ttk.Scrollbar(self.parent,orient="vertical",command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=scrollbar.set)

		self.content_frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0,0),window=self.content_frame,anchor="nw")
		self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.content_frame.bbox("all")))

		self.canvas.grid(row=0,column=0,sticky="nsew")
		scrollbar.grid(row=0, column=1, sticky="ns")

		self.parent.columnconfigure(0, weight=1)
		self.parent.rowconfigure(0, weight=1)
		self.content_frame.columnconfigure(0, weight=1)
		self.content_frame.rowconfigure(0, weight=1)

		cat0 = ttk.Label(self.content_frame, text="", borderwidth=1, relief="solid", width=20)
		self.windower.append(cat0)
		for a in categories:
			self.windower.append(ttk.Label(self.content_frame, text=a, borderwidth=1, relief="solid", width=20))
		for a in range(0, len(categories) + 1):
			self.windower[a].grid(row=0, column=a)

		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

	def _on_mousewheel(self,event):
		self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	def addApp(self):
		self.grids = [[], [], [], [], [], []]
		precision,rappel,stuff=self.rewardedStat()
		for a in range(len(self.application_data[0])):
		#for a in range(5):
			k = len(self.application_data[0]) - 1
			self.grids[0].append(ttk.Label(self.content_frame, text=str(self.application_data[0][a][0]), borderwidth=1, relief="solid", width=40,background=self.application_data[0][a][1]))
			self.grids[1].append(ttk.Label(self.content_frame, text=str(self.application_data[1][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[1][a][1]))
			self.grids[2].append(ttk.Label(self.content_frame, text=str(self.application_data[2][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[2][a][1]))
			self.grids[3].append(ttk.Label(self.content_frame, text=str(self.application_data[3][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[3][a][1]))
			self.grids[4].append(ttk.Label(self.content_frame, text=str(self.application_data[4][a][0]), borderwidth=1, relief="solid",width=20, background=self.application_data[4][a][1]))

			self.grids[0][a].grid(row=a + 1, column=0)
			self.grids[1][a].grid(row=a + 1, column=1)
			self.grids[2][a].grid(row=a + 1, column=2)
			self.grids[3][a].grid(row=a + 1, column=3)
			self.grids[4][a].grid(row=a + 1, column=4)

		NP = ttk.Label(self.content_frame, text="precision",relief="solid",width=40)
		NP1 = ttk.Label(self.content_frame,text=str(precision[0]))
		NP2 = ttk.Label(self.content_frame, text=str(precision[1]))
		NP3 = ttk.Label(self.content_frame, text=str(precision[2]))
		NP4 = ttk.Label(self.content_frame, text=str(precision[3]))

		NR = ttk.Label(self.content_frame, text="rappel", relief="solid", width=40)
		NR1 = ttk.Label(self.content_frame, text=str(rappel[0]))
		NR2 = ttk.Label(self.content_frame, text=str(rappel[1]))
		NR3 = ttk.Label(self.content_frame, text=str(rappel[2]))
		NR4 = ttk.Label(self.content_frame, text=str(rappel[3]))

		VN = ttk.Label(self.content_frame,text="vrai negatif",relief="solid",width=40)
		VN1 = ttk.Label(self.content_frame,text=str(stuff[0][0]))
		VN2 = ttk.Label(self.content_frame, text=str(stuff[1][0]))
		VN3 = ttk.Label(self.content_frame, text=str(stuff[2][0]))
		VN4 = ttk.Label(self.content_frame, text=str(stuff[3][0]))

		FN = ttk.Label(self.content_frame,text="faux negatif",relief="solid",width=40)
		FN1 = ttk.Label(self.content_frame,text=str(stuff[0][1]))
		FN2 = ttk.Label(self.content_frame, text=str(stuff[1][1]))
		FN3 = ttk.Label(self.content_frame, text=str(stuff[2][1]))
		FN4 = ttk.Label(self.content_frame, text=str(stuff[3][1]))

		VP = ttk.Label(self.content_frame,text="vrai positif",relief="solid",width=40)
		VP1 = ttk.Label(self.content_frame,text=str(stuff[0][2]))
		VP2 = ttk.Label(self.content_frame, text=str(stuff[1][2]))
		VP3 = ttk.Label(self.content_frame, text=str(stuff[2][2]))
		VP4 = ttk.Label(self.content_frame, text=str(stuff[3][2]))

		FP = ttk.Label(self.content_frame,text="faux positif",relief="solid",width=40)
		FP1 = ttk.Label(self.content_frame,text=str(stuff[0][3]))
		FP2 = ttk.Label(self.content_frame, text=str(stuff[1][3]))
		FP3 = ttk.Label(self.content_frame, text=str(stuff[2][3]))
		FP4 = ttk.Label(self.content_frame, text=str(stuff[3][3]))

		NP.grid(row=k+2,column=0)
		NP1.grid(row=k+2,column=1)
		NP2.grid(row=k+2,column=2)
		NP3.grid(row=k+2,column=3)
		NP4.grid(row=k + 2, column=4)

		NR.grid(row=k+3,column=0)
		NR1.grid(row=k+3,column=1)
		NR2.grid(row=k+3,column=2)
		NR3.grid(row=k+3,column=3)
		NR4.grid(row=k + 3, column=4)

		VN.grid(row=k+4,column=0)
		VN1.grid(row=k+4,column=1)
		VN2.grid(row=k+4,column=2)
		VN3.grid(row=k+4,column=3)
		VN4.grid(row=k + 4, column=4)

		FN.grid(row=k+5,column=0)
		FN1.grid(row=k+5,column=1)
		FN2.grid(row=k+5,column=2)
		FN3.grid(row=k+5,column=3)
		FN4.grid(row=k + 5, column=4)

		VP.grid(row=k+6,column=0)
		VP1.grid(row=k+6,column=1)
		VP2.grid(row=k+6,column=2)
		VP3.grid(row=k+6,column=3)
		VP4.grid(row=k + 6, column=4)

		FP.grid(row=k+7,column=0)
		FP1.grid(row=k+7,column=1)
		FP2.grid(row=k+7,column=2)
		FP3.grid(row=k+7,column=3)
		FP4.grid(row=k + 7, column=4)
		#print("==================ads")

		#self.grids[0][k].grid(row=a + 1, column=0)

	def update(self,data):
		#TODO: for loop is useless and waste memory
		for a in range(len(data[0])):
			self.application_data=copy.deepcopy(data)
		#print("ads updated")

	def reset(self):
		print("reset ads")
		for widget in self.content_frame.winfo_children():
			print("deleting:",widget)
			widget.destroy()
		self.build_ui()

