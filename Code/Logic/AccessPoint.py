from enum import IntEnum, unique


class __AccessPoint():
	AP_dict = dict()

	@unique
	class AP_ID(IntEnum):
		UI = 1
		Components = 2
		Constants = 3
		Scripts = 4

	class UI():
		def __init__(self):
			from Code.UI.MainWindow import MainWindow

			# Singleton variable
			self.MainWindow = MainWindow()

	class Components():
		def __init__(self):
			from Code.UI.Components.IconButton import IconButton

			# Not singleton variable
			self.IconButton = IconButton

	class Constants():
		def __init__(self):
			from Code.Utils.Constants.Coordinate import Coordinate
			from Code.Utils.Constants.Path import Path

			# Singleton variable
			self.Coordinate = Coordinate()
			# Singleton variable
			self.Path = Path()

	class Scripts():
		def __init__(self):
			from Code.Utils.Scripts.DataScripts import DataScripts

			# Static variable
			self.Data = DataScripts

	def getUI(self) -> UI:
		return self.AP_dict.setdefault(self.AP_ID.UI, self.UI())

	def getComponents(self) -> Components:
		return self.AP_dict.setdefault(self.AP_ID.Components, self.Components())

	def getConst(self) -> Constants:
		return self.AP_dict.setdefault(self.AP_ID.Constants, self.Constants())
	
	def getScripts(self) -> Scripts:
		return self.AP_dict.setdefault(self.AP_ID.Scripts, self.Scripts())

global AP
AP = __AccessPoint()
