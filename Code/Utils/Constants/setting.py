import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path


class Setting(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Инициализация данных Setting...')
		file_path = Path().setting_path
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Инициализация завершена')

	def __read_conf(self):
		if 'current' in self.__config:
			self.theme = self.__config.get('current', 'theme')
			self.language = self.__config.get('current', 'language')
			self.MaximumVelocity = self.__config.getfloat('current', 'MaximumVelocity', fallback=0.15)
			self.DecelerationFactor = self.__config.getfloat('current', 'DecelerationFactor', fallback=0.25)
			self.MousePressEventDelay = self.__config.getfloat('current', 'MousePressEventDelay', fallback=0.5)
		else:
			logging.critical('Секция "current" не найдена')
