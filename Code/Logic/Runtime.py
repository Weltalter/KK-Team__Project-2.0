from Code.Logic.AccessPoint import AP


class Runtime():
	def __init__(self):
		self.window = AP.Get_AP_UI().MainWindow__UI

	def Run(self):
		self.window.show()
