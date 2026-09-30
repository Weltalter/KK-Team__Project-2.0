import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Message(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Message": Инициализация...')
		file_path = Path().language_path

		self.__current_language = Setting().language_title
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Модуль "Message": Инициализация завершена')

	def __read_conf(self):
		if 'language' in self.__config:
			self.m_languages = [self.__config.get('language', f'language_{i}') for i in range(len(self.__config['language'].keys() - self.__config['DEFAULT'].keys()))]

		if f'{self.__current_language}.swipes' in self.__config:
			self.m_swipes = [self.__config.get(f'{self.__current_language}.swipes', f'swipe_{i}') for i in range(len(self.__config[f'{self.__current_language}.swipes'].keys()))]
		else:
			logging.critical(f'Секция "{self.__current_language}.swipes" не найдена')

		if f'{self.__current_language}' in self.__config:
			self.m_version = self.__config.get(f'{self.__current_language}', 'version')
		else:
			logging.critical(f'Секция "{self.__current_language}" не найдена')
