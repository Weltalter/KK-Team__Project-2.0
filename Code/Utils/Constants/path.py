import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton


class Path(metaclass=MetaSingleton):
	path: str = 'DataFile/Files.ini/path.ini'
	def __init__(self):
		logging.info('Модуль "Path": Инициализация...')
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(self.path, encoding='utf-8')

		self.__read_conf()
		logging.info('Модуль "Path": Инициализация завершена')


	def __read_conf(self):
		if 'files' in self.__config:
			self.coordinate_path = self.__config.get('files', 'coordinate_file')
			self.language_path = self.__config.get('files', 'language_file')
			self.setting_path = self.__config.get('files', 'setting_file')
			self.theme_path = self.__config.get('files', 'theme_file')
			self.icon_path = self.__config.get('files', 'icon_file')
		else:
			logging.critical('Секция "files" не найдена')
		
		self.font_dir_path = self.__config.get('DEFAULT', 'main_font_dir')
