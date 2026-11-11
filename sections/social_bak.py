import copy
from tkinter import ttk, Canvas


class Social(ttk.Frame):
	application_data = [[], []]
	grids = [[], [], []]

	windower = []

	falseP = 0
	trueP = 0
	falseN = 0
	trueN = 0

	def rewardedStat(self):
		falseP=0
		trueP=0
		falseN=0
		trueN=0
		precisionData=[-1.0]
		rappelData=[-1.0]
		stuff=[]
		for a in range(1,len(self.application_data)):
			s = self.application_data[a]
			for d in s:
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
		return precisionData,rappelData,stuff

	def __init__(self, parent):
		super().__init__()
		categories = ["Leaderboard"]
		self.windower = []
		#cat0 = ttk.Label(parent, text="", borderwidth=1, relief="solid", width=20)
		#self.windower.append(cat0)
		#for a in categories:
		#	self.windower.append(ttk.Label(parent, text=a, borderwidth=1, relief="solid", width=20))
		#print(len(self.windower))
		#for a in range(0, len(categories) + 1):
		#	self.windower[a].grid(row=0, column=a)

		self.canvas = Canvas(parent)
		scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=scrollbar.set)

		self.content_frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
		self.content_frame.bind("<Configure>",lambda e: self.canvas.configure(scrollregion=self.content_frame.bbox("all")))

		self.canvas.grid(row=0, column=0, sticky="nsew")
		scrollbar.grid(row=0, column=1, sticky="ns")

		parent.columnconfigure(0, weight=1)
		parent.rowconfigure(0, weight=1)
		self.content_frame.columnconfigure(0, weight=1)
		self.content_frame.rowconfigure(0, weight=1)

		cat0 = ttk.Label(self.content_frame, text="", borderwidth=1, relief="solid", width=20)
		self.windower.append(cat0)
		for a in categories:
			self.windower.append(ttk.Label(self.content_frame, text=a, borderwidth=1, relief="solid", width=20))
		for a in range(0, len(categories) + 1):
			self.windower[a].grid(row=0, column=a)

		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	def addApp(self, parent):
		precision, rappel,stuff = self.rewardedStat()
		for a in range(len(self.application_data[0])):
			k = len(self.application_data[0]) - 1
			self.grids[0].append(ttk.Label(self.content_frame, text=str(self.application_data[0][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[0][a][1]))
			self.grids[1].append(ttk.Label(self.content_frame, text=str(self.application_data[1][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[1][a][1]))

			self.grids[0][a].grid(row=a + 1, column=0)
			self.grids[1][a].grid(row=a + 1, column=1)

		NP = ttk.Label(self.content_frame, text="precision", relief="solid", width=40)
		NP1 = ttk.Label(self.content_frame, text=str(precision[0]))

		NR = ttk.Label(self.content_frame, text="rappel", relief="solid", width=40)
		NR1 = ttk.Label(self.content_frame, text=str(rappel[0]))

		VN = ttk.Label(self.content_frame, text="vrai negatif", relief="solid", width=40)
		VN1 = ttk.Label(self.content_frame, text=str(stuff[0][0]))

		FN = ttk.Label(self.content_frame, text="faux negatif", relief="solid", width=40)
		FN1 = ttk.Label(self.content_frame, text=str(stuff[0][1]))

		VP = ttk.Label(self.content_frame, text="vrai positif", relief="solid", width=40)
		VP1 = ttk.Label(self.content_frame, text=str(stuff[0][2]))

		FP = ttk.Label(self.content_frame, text="faux positif", relief="solid", width=40)
		FP1 = ttk.Label(self.content_frame, text=str(stuff[0][3]))

		NP.grid(row=k + 2, column=0)
		NP1.grid(row=k + 2, column=1)

		NR.grid(row=k + 3, column=0)
		NR1.grid(row=k + 3, column=1)

		VN.grid(row=k + 4, column=0)
		VN1.grid(row=k + 4, column=1)

		FN.grid(row=k + 5, column=0)
		FN1.grid(row=k + 5, column=1)

		VP.grid(row=k + 6, column=0)
		VP1.grid(row=k + 6, column=1)

		FP.grid(row=k + 7, column=0)
		FP1.grid(row=k + 7, column=1)

	def update(self, data):
		for a in range(len(data[0])):
			self.application_data = copy.deepcopy(data)
		#print("social done")