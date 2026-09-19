from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.libraries import *
from Code.UI.main_window import MainWindow

class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		pass

	def run(self):
		self.test = MainWindow()
		self.test.show()

