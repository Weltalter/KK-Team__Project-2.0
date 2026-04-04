from Code.Logic.AccessPoint import AP
from configparser import ConfigParser, ExtendedInterpolation


class Coordinate():
	def __init__(self):
		data = ConfigParser(interpolation=ExtendedInterpolation())
		data.read("DataFile/Files.ini/Coordinate/MainWindow.ini", encoding='utf-8')
		self.__MainWindow = AP.Get_Scripts().Data.items_to_dict(items=data.items('MainWindow'),
														   		type=int)

	def get__MainWindow(self):
		return self.__MainWindow
