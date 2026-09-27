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
			self.i_swipe_0 = self.__config.get('swipes', 'swipe_0')
			self.i_swipe_1 = self.__config.get('swipes', 'swipe_1')
			self.i_swipe_2 = self.__config.get('swipes', 'swipe_2')
			self.i_swipe_3 = self.__config.get('swipes', 'swipe_3')
			self.i_swipe_4 = self.__config.get('swipes', 'swipe_4')
			self.i_swipe_5 = self.__config.get('swipes', 'swipe_5')
			self.i_swipe_6 = self.__config.get('swipes', 'swipe_6')
			self.i_swipe_7 = self.__config.get('swipes', 'swipe_7')
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
			self.i_theme_0 = self.__config.get('theme', 'theme_0')
			self.i_theme_1 = self.__config.get('theme', 'theme_1')
			self.i_theme_2 = self.__config.get('theme', 'theme_2')
		else:
			logging.critical('Секция "theme" не найдена')
