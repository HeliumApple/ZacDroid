import copy
from pickle import FALSE
from tkinter import ttk, Canvas, LEFT, BOTH, VERTICAL, RIGHT, Y
from tkinter.ttk import Scrollbar

import Model
#import ModelLinux


class test2(ttk.Frame):
	application_data = [[],[], [], [], [],[],[],[],[]]
	grids = [[],[], [], [], [], [],[],[],[]]

	falseP = 0
	trueP = 0
	falseN = 0
	trueN = 0

	windower = []


	def rewardedStat(self):
		precisionData=[-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
		rappelData=[-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
		stuff=[]
		for a in range(1,len(self.application_data)):
			falseP = 0
			trueP = 0
			falseN = 0
			trueN = 0
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
			#print("trueP=", trueP, "falseP=", falseP, "trueN=", trueN, "falseN=", falseN)
		return precisionData,rappelData,stuff

	def __init__(self,parent):
		super().__init__()

		self.canvas=Canvas(parent)
		self.parent=parent

		self.build_ui()

	def build_ui(self):
		self.canvas = Canvas(self.parent)
		categories = [Model.test9, Model.test10, Model.test11,Model.test12,Model.test13,Model.test14,Model.test15,Model.test16]
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
		self.grids = [[], [], [], [], [], [], [], [], []]
		precision,rappel,stuff=self.rewardedStat()
		for a in range(len(self.application_data[0])):
			k = len(self.application_data[0]) - 1
			self.grids[0].append(ttk.Label(self.content_frame, text=str(self.application_data[0][a][0]), borderwidth=1, relief="solid", width=40,background=self.application_data[0][a][1]))
			self.grids[1].append(ttk.Label(self.content_frame, text=str(self.application_data[1][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[1][a][1]))
			self.grids[2].append(ttk.Label(self.content_frame, text=str(self.application_data[2][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[2][a][1]))
			self.grids[3].append(ttk.Label(self.content_frame, text=str(self.application_data[3][a][0]), borderwidth=1, relief="solid", width=20,background=self.application_data[3][a][1]))
			self.grids[4].append(ttk.Label(self.content_frame, text=str(self.application_data[4][a][0]), borderwidth=1, relief="solid",width=20, background=self.application_data[4][a][1]))
			self.grids[5].append(ttk.Label(self.content_frame, text=str(self.application_data[5][a][0]), borderwidth=1, relief="solid",width=20, background=self.application_data[5][a][1]))
			self.grids[6].append(ttk.Label(self.content_frame, text=str(self.application_data[6][a][0]), borderwidth=1, relief="solid",width=20, background=self.application_data[6][a][1]))
			self.grids[7].append(ttk.Label(self.content_frame, text=str(self.application_data[7][a][0]), borderwidth=1, relief="solid", width=20, background=self.application_data[7][a][1]))
			self.grids[8].append(ttk.Label(self.content_frame, text=str(self.application_data[8][a][0]), borderwidth=1, relief="solid",width=20, background=self.application_data[8][a][1]))


			self.grids[0][a].grid(row=a + 1, column=0)
			self.grids[1][a].grid(row=a + 1, column=1)
			self.grids[2][a].grid(row=a + 1, column=2)
			self.grids[3][a].grid(row=a + 1, column=3)
			self.grids[4][a].grid(row=a + 1, column=4)
			self.grids[5][a].grid(row=a + 1, column=5)
			self.grids[6][a].grid(row=a + 1, column=6)
			self.grids[7][a].grid(row=a + 1, column=7)
			self.grids[8][a].grid(row=a + 1, column=8)

		NP = ttk.Label(self.content_frame, text="precision",relief="solid",width=40)
		NP1 = ttk.Label(self.content_frame,text=str(precision[0]))
		NP2 = ttk.Label(self.content_frame, text=str(precision[1]))
		NP3 = ttk.Label(self.content_frame, text=str(precision[2]))
		NP4 = ttk.Label(self.content_frame, text=str(precision[3]))
		NP5 = ttk.Label(self.content_frame, text=str(precision[4]))
		NP6 = ttk.Label(self.content_frame, text=str(precision[5]))
		NP7 = ttk.Label(self.content_frame, text=str(precision[6]))
		NP8 = ttk.Label(self.content_frame, text=str(precision[7]))

		NR = ttk.Label(self.content_frame, text="rappel", relief="solid", width=40)
		NR1 = ttk.Label(self.content_frame, text=str(rappel[0]))
		NR2 = ttk.Label(self.content_frame, text=str(rappel[1]))
		NR3 = ttk.Label(self.content_frame, text=str(rappel[2]))
		NR4 = ttk.Label(self.content_frame, text=str(rappel[3]))
		NR5 = ttk.Label(self.content_frame, text=str(rappel[4]))
		NR6 = ttk.Label(self.content_frame, text=str(rappel[5]))
		NR7 = ttk.Label(self.content_frame, text=str(rappel[6]))
		NR8 = ttk.Label(self.content_frame, text=str(rappel[7]))

		VN = ttk.Label(self.content_frame, text="vrai negatif", relief="solid", width=40)
		VN1 = ttk.Label(self.content_frame, text=str(stuff[0][0]))
		VN2 = ttk.Label(self.content_frame, text=str(stuff[1][0]))
		VN3 = ttk.Label(self.content_frame, text=str(stuff[2][0]))
		VN4 = ttk.Label(self.content_frame, text=str(stuff[3][0]))
		VN5 = ttk.Label(self.content_frame, text=str(stuff[4][0]))
		VN6 = ttk.Label(self.content_frame, text=str(stuff[5][0]))
		VN7 = ttk.Label(self.content_frame, text=str(stuff[6][0]))
		VN8 = ttk.Label(self.content_frame, text=str(stuff[7][0]))

		FN = ttk.Label(self.content_frame, text="faux negatif", relief="solid", width=40)
		FN1 = ttk.Label(self.content_frame, text=str(stuff[0][1]))
		FN2 = ttk.Label(self.content_frame, text=str(stuff[1][1]))
		FN3 = ttk.Label(self.content_frame, text=str(stuff[2][1]))
		FN4 = ttk.Label(self.content_frame, text=str(stuff[3][1]))
		FN5 = ttk.Label(self.content_frame, text=str(stuff[4][1]))
		FN6 = ttk.Label(self.content_frame, text=str(stuff[5][1]))
		FN7 = ttk.Label(self.content_frame, text=str(stuff[6][1]))
		FN8 = ttk.Label(self.content_frame, text=str(stuff[7][1]))

		VP = ttk.Label(self.content_frame, text="vrai positif", relief="solid", width=40)
		VP1 = ttk.Label(self.content_frame, text=str(stuff[0][2]))
		VP2 = ttk.Label(self.content_frame, text=str(stuff[1][2]))
		VP3 = ttk.Label(self.content_frame, text=str(stuff[2][2]))
		VP4 = ttk.Label(self.content_frame, text=str(stuff[3][2]))
		VP5 = ttk.Label(self.content_frame, text=str(stuff[4][2]))
		VP6 = ttk.Label(self.content_frame, text=str(stuff[5][2]))
		VP7 = ttk.Label(self.content_frame, text=str(stuff[6][2]))
		VP8 = ttk.Label(self.content_frame, text=str(stuff[7][2]))

		FP = ttk.Label(self.content_frame, text="faux positif", relief="solid", width=40)
		FP1 = ttk.Label(self.content_frame, text=str(stuff[0][3]))
		FP2 = ttk.Label(self.content_frame, text=str(stuff[1][3]))
		FP3 = ttk.Label(self.content_frame, text=str(stuff[2][3]))
		FP4 = ttk.Label(self.content_frame, text=str(stuff[3][3]))
		FP5 = ttk.Label(self.content_frame, text=str(stuff[4][3]))
		FP6 = ttk.Label(self.content_frame, text=str(stuff[5][3]))
		FP7 = ttk.Label(self.content_frame, text=str(stuff[6][3]))
		FP8 = ttk.Label(self.content_frame, text=str(stuff[7][3]))

		NP.grid(row=k+2,column=0)
		NP1.grid(row=k+2,column=1)
		NP2.grid(row=k+2,column=2)
		NP3.grid(row=k+2,column=3)
		NP4.grid(row=k + 2, column=4)
		NP5.grid(row=k + 2, column=5)
		NP6.grid(row=k + 2, column=6)
		NP7.grid(row=k + 2, column=7)
		NP8.grid(row=k + 2, column=8)

		NR.grid(row=k+3,column=0)
		NR1.grid(row=k+3,column=1)
		NR2.grid(row=k+3,column=2)
		NR3.grid(row=k+3,column=3)
		NR4.grid(row=k + 3, column=4)
		NR5.grid(row=k + 3, column=5)
		NR6.grid(row=k + 3, column=6)
		NR7.grid(row=k + 3, column=7)
		NR8.grid(row=k + 3, column=8)

		VN.grid(row=k + 4, column=0)
		VN1.grid(row=k + 4, column=1)
		VN2.grid(row=k + 4, column=2)
		VN3.grid(row=k + 4, column=3)
		VN4.grid(row=k + 4, column=4)
		VN5.grid(row=k + 4, column=5)
		VN6.grid(row=k + 4, column=6)
		VN7.grid(row=k + 4, column=7)
		VN8.grid(row=k + 4, column=8)

		FN.grid(row=k + 5, column=0)
		FN1.grid(row=k + 5, column=1)
		FN2.grid(row=k + 5, column=2)
		FN3.grid(row=k + 5, column=3)
		FN4.grid(row=k + 5, column=4)
		FN5.grid(row=k + 5, column=5)
		FN6.grid(row=k + 5, column=6)
		FN7.grid(row=k + 5, column=7)
		FN8.grid(row=k + 5, column=8)

		VP.grid(row=k + 6, column=0)
		VP1.grid(row=k + 6, column=1)
		VP2.grid(row=k + 6, column=2)
		VP3.grid(row=k + 6, column=3)
		VP4.grid(row=k + 6, column=4)
		VP5.grid(row=k + 6, column=5)
		VP6.grid(row=k + 6, column=6)
		VP7.grid(row=k + 6, column=7)
		VP8.grid(row=k + 6, column=8)

		FP.grid(row=k + 7, column=0)
		FP1.grid(row=k + 7, column=1)
		FP2.grid(row=k + 7, column=2)
		FP3.grid(row=k + 7, column=3)
		FP4.grid(row=k + 7, column=4)
		FP5.grid(row=k + 7, column=5)
		FP6.grid(row=k + 7, column=6)
		FP7.grid(row=k + 7, column=7)
		FP8.grid(row=k + 7, column=8)
		#print("==================ads")

		#self.grids[0][k].grid(row=a + 1, column=0)

	def update(self,data):
		#TODO: for loop is useless and waste memory
		for a in range(len(data[0])):
			self.application_data=copy.deepcopy(data)
		#print("test2 done")

	def reset(self):
		#print("reset test2")
		for widget in self.content_frame.winfo_children():
			widget.destroy()
		self.build_ui()