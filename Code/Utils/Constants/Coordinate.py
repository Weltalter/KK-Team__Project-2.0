from Code.Logic.AccessPoint import AP
from configparser import ConfigParser, ExtendedInterpolation


class Coordinate():
	def __init__(self):
		data = ConfigParser(interpolation=ExtendedInterpolation())
		data.read("DataFile/Files.ini/Coordinate/MainWindow.ini", encoding='utf-8')
		self.__main_window = AP.getScripts().Data.itemsToDict(items=data.items('MainWindow'),
														   	type=int,
															coordinate_flag=True)

	def get__main_window(self):
		return self.__main_window
