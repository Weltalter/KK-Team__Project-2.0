from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.libraries import *
from Code.UI.main_window import MainWindow
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.theme import Theme



class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		path = Path()
		setting = Setting()
		theme = Theme()

	def run(self):
		self.test = MainWindow()
		self.test.show()

