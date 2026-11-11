import tkinter as tk #removed TK
import exporter #removed TK
from View import View
from loguru import logger #removeTK
from contextlib import contextmanager

import loguru

import Truths
from Controller import Controller
from Model import Model
from View import View
from loguru import logger #removeTK

@contextmanager
def loguru_disable(name):
    loguru.logger.disable(name)
    try:
        yield
    finally:
        loguru.logger.enable(name)



@loguru_disable("androguard") #removed TK
class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('new')

		model = Model()
		view = View(self)
		#view.grid(row=0,column=0,padx=10,pady=10)

		controller = Controller(model,view)
		view.set_controller(controller)

class App_linux():
	def __init__(self):
		model=Model()
		# view=View(self)
		controller = Controller(model,None)
		# view = View(self)
		# view.set_controller(controller)
		self.controller=Controller(model,None)

		super().__init__()
		# self.title('new')

		model = Model()
		# view = View(self)

		# view.grid(row=0,column=0,padx=10,pady=10)

		controller = Controller(model, None)
		# view.set_controller(controller)

if __name__ == '__main__':
	# app=App_linux()
	# folder="../final_apps_decomp_deobf/"
	# app.controller.analyse_cli(folder)

	app = App()
	app.mainloop()

