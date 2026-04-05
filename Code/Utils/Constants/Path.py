from Code.Logic.AccessPoint import AP
from configparser import ConfigParser, ExtendedInterpolation


class Path():
	def __init__(self):
		data = ConfigParser(interpolation=ExtendedInterpolation())
		data.read("DataFile/Files.ini/Path.ini", encoding='utf-8')
		self.__files_ini = AP.getScripts().Data.itemsToDict(items=data.items('Files.ini'),
														  	type=str)

	def get__files_ini(self):
		return self.__files_ini
