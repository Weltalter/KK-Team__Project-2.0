import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Message(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Message": Инициализация...')
		file_path = Path().language_path

		self.__current_language = Setting().language
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Модуль "Message": Инициализация завершена')

	def __read_conf(self):
		if 'russian.swipes' in self.__config:
			self.m_swipes = [self.__config.get('russian.swipes', f'swipe_{i}') for i in range(len(self.__config['russian.swipes'].keys()))]
		else:
			logging.critical('Секция "russian.swipes" не найдена')

		if 'russian' in self.__config:
			self.m_version = self.__config.get('russian', 'version')
		else:
			logging.critical('Секция "russian" не найдена')
