import copy
from tkinter import ttk, Canvas
from tkinter.ttk import Scrollbar


class ads(ttk.Frame):
	application_data = [[], [], [], [], [], []]
	grids = [[], [], [], [], [], []]
	windower = []

	def __init__(self, parent):
		super().__init__(parent)
		categories = ["rewarded", "Interstitial", "offerwall"]
		self.windower = []

		# Create header labels
		cat0 = ttk.Label(self, text="", borderwidth=1, relief="solid", width=20)
		self.windower.append(cat0)
		for a in categories:
			self.windower.append(ttk.Label(self, text=a, borderwidth=1, relief="solid", width=20))

		for a in range(0, len(categories) + 1):
			self.windower[a].grid(row=0, column=a)

		# Create a Canvas for scrolling
		self.canvas = Canvas(self)
		self.canvas.grid(row=1, column=0, columnspan=len(categories) + 1, sticky="nsew")

		# Add vertical scrollbar
		scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
		scrollbar.grid(row=1, column=len(categories) + 1, sticky="ns")
		self.canvas.configure(yscrollcommand=scrollbar.set)

		# Create a frame inside the canvas to hold the content
		self.content_frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

		# Configure the frame to expand and adjust scrolling region
		self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

		# Enable mouse wheel scrolling
		self.bind_all("<MouseWheel>", self._on_mousewheel)

		# Configure column and row expansion
		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

	def addApp(self):
		for a in range(len(self.application_data[0])):
			self.grids[0].append(
				ttk.Label(self.content_frame, text=str(self.application_data[0][a][0]), borderwidth=1, relief="solid",
				          width=40, background=self.application_data[0][a][1]))
			self.grids[1].append(
				ttk.Label(self.content_frame, text=str(self.application_data[1][a][0]), borderwidth=1, relief="solid",
				          width=20, background=self.application_data[1][a][1]))
			self.grids[2].append(
				ttk.Label(self.content_frame, text=str(self.application_data[2][a][0]), borderwidth=1, relief="solid",
				          width=20, background=self.application_data[2][a][1]))
			self.grids[3].append(
				ttk.Label(self.content_frame, text=str(self.application_data[3][a][0]), borderwidth=1, relief="solid",
				          width=20, background=self.application_data[3][a][1]))

			self.grids[0][a].grid(row=a + 1, column=0)
			self.grids[1][a].grid(row=a + 1, column=1)
			self.grids[2][a].grid(row=a + 1, column=2)
			self.grids[3][a].grid(row=a + 1, column=3)

	def update(self, data):
		self.application_data = copy.deepcopy(data)
		self.addApp()
