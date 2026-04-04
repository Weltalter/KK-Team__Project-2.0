from enum import IntEnum, unique


class __AccessPoint():
	AP_Dict = dict()

	@unique
	class AP_ID(IntEnum):
		AP_UI = 1
		AP_Constants = 2
		AP_Scripts = 3

	class UI_AccessPoint():
		def __init__(self):
			from Code.UI.MainWindow import MainWindow

			self.MainWindow = MainWindow()

	class Constants_AccessPoint():
		def __init__(self):
			from Code.Utils.Constants.Coordinate import Coordinate
			from Code.Utils.Constants.Path import Path

			self.Coordinate = Coordinate()
			self.Path = Path()

	class Scripts_AccessPoint():
		def __init__(self):
			from Code.Utils.Scripts.DataScripts import DataScripts
			
			self.Data = DataScripts

	def Get_UI(self) -> UI_AccessPoint:
		return self.AP_Dict.setdefault(self.AP_ID.AP_UI, self.UI_AccessPoint())

	def Get_Const(self) -> Constants_AccessPoint:
		return self.AP_Dict.setdefault(self.AP_ID.AP_Constants, self.Constants_AccessPoint())
	
	def Get_Scripts(self) -> Scripts_AccessPoint:
		return self.AP_Dict.setdefault(self.AP_ID.AP_Scripts, self.Scripts_AccessPoint())

global AP
AP = __AccessPoint()
