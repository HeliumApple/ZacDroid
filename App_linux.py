# import tkinter as tk #removed TK
# import exporter #removed TK
# from View import View
# from loguru import logger #removeTK
from contextlib import contextmanager

import loguru

import Truths
from Controller import Controller
from Model import Model
#from ModelLinux import ModelLinux
# from View import View
# from loguru import logger #removeTK

CLI=False
if not CLI:
	"""GUI not used"""
	import tkinter as tk #removed TK
	import exporter #removed TK
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
		self.controller=Controller(model,None)

		super().__init__()

if __name__ == '__main__':
	if CLI:
		app=App_linux()
		folder="../finap_apps_apk_free/decompiled_work_dir/jadx_decompiled/"
		app.controller.analyse_cli(folder)
	else:
		app = App()
		app.mainloop()


