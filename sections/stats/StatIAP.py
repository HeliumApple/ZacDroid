import copy
from tkinter import ttk

class StatIAP(ttk.Frame):
	application_data=[[], [], []]
	grids=[[],[],[],[],[],[]]

	windower = []
	def __init__(self,parent):
		super().__init__()
		categories=["rappel","précision"]
		self.windower=[]
		cat0 = ttk.Label(parent, text="", borderwidth=1, relief="solid", width=20)
		self.windower.append(cat0)
		for a in categories:
			self.windower.append(ttk.Label(parent,text=a,borderwidth=1, relief="solid", width=20))
		#print(len(self.windower))
		for a in range(0,len(categories)+1):
			self.windower[a].grid(row=0,column=a)


	def addApp(self,parent):
		for a in range(len(self.application_data[1])):
			#print(self.application_data[0])
			#print(self.application_data[0])
			self.grids[0].append(ttk.Label(parent, text=str(self.application_data[0][a]), borderwidth=1, relief="solid", width=40))#,background=self.application_data[0][a][1]))
			self.grids[1].append(ttk.Label(parent, text=str(self.application_data[1][a]), borderwidth=1, relief="solid", width=20))#,background=self.application_data[1][a][1]))
			self.grids[2].append(ttk.Label(parent, text=str(self.application_data[2][a]), borderwidth=1, relief="solid", width=20))#,background=self.application_data[2][a][1]))

			#self.grids[0][a].grid(row=a + 1, column=0)
			#self.grids[1][a].grid(row=a + 1, column=1)
			#self.grids[2][a].grid(row=a + 1, column=2)


	def update(self,data):
		for a in range(len(data[0])):
			self.application_data=copy.deepcopy(data)
		#print(data)