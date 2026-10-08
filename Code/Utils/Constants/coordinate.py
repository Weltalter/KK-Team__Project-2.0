import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path


class Coordinate(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Coordinate": Инициализация...')
		file_path = Path().coordinate_path
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Модуль "Coordinate": Инициализация завершена')

	def __read_conf(self):
		if 'main_window' in self.__config:
			self.window_x = self.__config.getint('main_window', 'x')
			self.window_y = self.__config.getint('main_window', 'y')
			self.window_width = self.__config.getint('main_window', 'width')
			self.window_height = self.__config.getint('main_window', 'height')
		else:
			logging.critical('Секция "main_window" не найдена')

		if 'sidebar' in self.__config:
			self.sidebar_width = self.__config.getint('sidebar', 'width')
			self.sidebar_btn_size = self.__config.getint('sidebar', 'btn_size')
			self.sidebar_btn_x = self.__config.getint('sidebar', 'btn_x')
			self.sidebar_setting_btn_y = self.__config.getint('sidebar', 'btn_1_y')
			self.sidebar_export_btn_y = self.__config.getint('sidebar', 'btn_2_y')
			self.sidebar_import_btn_y = self.__config.getint('sidebar', 'btn_3_y')
			self.sidebar_exit_btn_y = self.__config.getint('sidebar', 'btn_4_y')
		else:
			logging.critical('Секция "sidebar" не найдена')

		if 'header' in self.__config:
			self.header_height = self.__config.getint('header', 'height')
			self.header_padding = self.__config.getint('header', 'padding')
			self.header_theme_btn_width = self.__config.getint('header', 'theme_btn_width')
			self.header_theme_btn_height = self.__config.getint('header', 'theme_btn_height')
			self.header_theme_btn_radius = self.__config.getint('header', 'theme_btn_radius')
			self.header_theme_btn_offset = self.__config.getint('header', 'theme_btn_offset')
		else:
			logging.critical('Секция "header" не найдена')
		
		if 'footer' in self.__config:
			self.footer_height = self.__config.getint('footer', 'height')
			self.footer_padding = self.__config.getint('footer', 'padding')
			self.footer_language_btn_width = self.__config.getint('footer', 'language_btn_width')
			self.footer_language_btn_height = self.__config.getint('footer', 'language_btn_height')
			self.footer_language_btn_radius = self.__config.getint('footer', 'language_btn_radius')
			self.footer_language_btn_offset = self.__config.getint('footer', 'language_btn_offset')
		else:
			logging.critical('Секция "footer" не найдена')

		if 'main_menu' in self.__config:
			self.main_menu_margin = self.__config.getint('main_menu', 'margin')
			self.main_menu_scroll_spacing = self.__config.getint('main_menu', 'scroll_spacing')
			self.main_menu_swipe_width = self.__config.getint('main_menu', 'swipe_width')
			self.main_menu_swipe_radius = self.__config.getint('main_menu', 'swipe_radius')
			self.main_menu_swipe_spacing = self.__config.getint('main_menu', 'swipe_spacing')
		else:
			logging.critical('Секция "main_menu" не найдена')
