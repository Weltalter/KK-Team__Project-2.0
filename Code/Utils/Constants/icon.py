import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Icon(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Icon": Инициализация...')
		file_path = Path().icon_path

		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(f'{file_path}', encoding='utf-8')

		self.__read_conf()
		logging.info('Модуль "Icon": Инициализация завершена')

	def __read_conf(self):
		if 'swipes' in self.__config:
			self.i_swipes = [self.__config.get('swipes', f'swipe_{i}') for i in range(len(self.__config['swipes'].keys() - self.__config['DEFAULT'].keys()))]
		else:
			logging.critical('Секция "swipes" не найдена')
		
		if 'sidebar' in self.__config:
			self.i_setting = self.__config.get('sidebar', 'setting')
			self.i_export = self.__config.get('sidebar', 'export')
			self.i_import = self.__config.get('sidebar', 'import')
			self.i_exit = self.__config.get('sidebar', 'exit')
		else:
			logging.critical('Секция "sidebar" не найдена')
		
		if 'theme' in self.__config:
			self.i_reload = self.__config.get('theme', 'reload')
			self.i_themes = [self.__config.get('theme', f'theme_{i}') for i in range(len(self.__config['theme'].keys() - self.__config['DEFAULT'].keys()) - 1)]
		else:
			logging.critical('Секция "theme" не найдена')
