from Code.Logic.AccessPoint import AP


class Runtime():
	def __init__(self):
		self.window = AP.getUI().MainWindow

	def run(self):
		self.window.show()
