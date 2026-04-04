from Code.UI.MainWindow import MainWindow
from enum import IntEnum, unique


class __AccessPoint():
	AP_Dict = dict()

	@unique
	class AP_ID(IntEnum):
		AP_UI = 1

	class UI_AccessPoint():
		def __init__(self):
			self.MainWindow__UI = MainWindow()

	def Get_AP_UI(self):
		return self.AP_Dict.setdefault(self.AP_ID.AP_UI, self.UI_AccessPoint())

global AP
AP = __AccessPoint()
