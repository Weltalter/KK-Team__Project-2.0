from Code.Logic.AccessPoint import AP


class Runtime():
	def __init__(self):
		self.window = AP.Get_UI().MainWindow

	def Run(self):
		self.window.show()
