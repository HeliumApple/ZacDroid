from tkinter import ttk, Canvas
import copy


class general(ttk.Frame):
	application_data=[[], [], [], [], [], [], [], []]
	grids=[[],[],[],[],[],[],[],[]]
	windower=[]
	def __init__(self, parent):
		super().__init__()
		categories=["Développeur","Année de publication","Nombre de téléchargement","Note appréciative","Catégorie","ESRB","Privacy policy"]
		self.windower=[]
		#cat0 = ttk.Label(parent, text="", borderwidth=1, relief="solid", width=20)
		#self.windower.append(cat0)
		#for a in categories:
		#	self.windower.append(ttk.Label(parent,text=a,borderwidth=1, relief="solid", width=20))
		#print(len(self.windower))
		#for a in range(0,len(categories)+1):
		#	self.windower[a].grid(row=0,column=a)

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

	def addApp(self,parent):
		for a in range(len(self.application_data[0])):
			self.grids[0].append(ttk.Label(self.content_frame, text=str(self.application_data[0][a]), borderwidth=1, relief="solid", width=20))
			self.grids[1].append(ttk.Label(self.content_frame, text=str(self.application_data[1][a]), borderwidth=1, relief="solid", width=20))
			self.grids[2].append(ttk.Label(self.content_frame, text=str(self.application_data[2][a]), borderwidth=1, relief="solid", width=20))
			self.grids[3].append(ttk.Label(self.content_frame, text=str(self.application_data[3][a]), borderwidth=1, relief="solid", width=20))
			self.grids[4].append(ttk.Label(self.content_frame, text=str(self.application_data[4][a]), borderwidth=1, relief="solid", width=20))
			self.grids[5].append(ttk.Label(self.content_frame, text=str(self.application_data[5][a]), borderwidth=1, relief="solid", width=20))
			self.grids[6].append(ttk.Label(self.content_frame, text=str(self.application_data[6][a]), borderwidth=1, relief="solid", width=20))
			self.grids[7].append(ttk.Label(self.content_frame, text=str(self.application_data[7][a]), borderwidth=1, relief="solid", width=20))

			self.grids[0][a].grid(row=a + 1, column=0)
			self.grids[1][a].grid(row=a + 1, column=1)
			self.grids[2][a].grid(row=a + 1, column=2)
			self.grids[3][a].grid(row=a + 1, column=3)
			self.grids[4][a].grid(row=a + 1, column=4)
			self.grids[5][a].grid(row=a + 1, column=5)
			self.grids[6][a].grid(row=a + 1, column=6)
			self.grids[7][a].grid(row=a + 1, column=7)

	def update(self,data):
		for a in range(len(data[0])):
			self.application_data=copy.deepcopy(data)
		#print("gen done")


