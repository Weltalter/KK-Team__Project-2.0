import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path


class Coordinate(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Coordinate": Инициализация...')
		file_path = Path().coordinate_path
		self._config = ConfigParser(interpolation=ExtendedInterpolation())
		self._config.read(file_path, encoding='utf-8')

		self._read_conf()
		logging.info('Модуль "Coordinate": Инициализация завершена')

	def _read_conf(self):
		if 'main_window' in self._config:
			self.window_x = self._config.getint('main_window', 'x')
			self.window_y = self._config.getint('main_window', 'y')
			self.window_width = self._config.getint('main_window', 'width')
			self.window_height = self._config.getint('main_window', 'height')
		else:
			logging.critical('Секция "main_window" не найдена')

		if 'sidebar' in self._config:
			self.sidebar_collapsed_width = self._config.getint('sidebar', 'collapsed_width')
			self.sidebar_expanded_width = self._config.getint('sidebar', 'expanded_width')
			self.sidebar_btn_size = self._config.getint('sidebar', 'btn_size')
			self.sidebar_btn_x = self._config.getint('sidebar', 'btn_x')
			self.sidebar_setting_btn_y = self._config.getint('sidebar', 'btn_1_y')
			self.sidebar_export_btn_y = self._config.getint('sidebar', 'btn_2_y')
			self.sidebar_import_btn_y = self._config.getint('sidebar', 'btn_3_y')
			self.sidebar_exit_btn_y = self._config.getint('sidebar', 'btn_4_y')
		else:
			logging.critical('Секция "sidebar" не найдена')

		if 'header' in self._config:
			self.header_height = self._config.getint('header', 'height')
			self.header_padding = self._config.getint('header', 'padding')
			self.header_theme_btn_width = self._config.getint('header', 'theme_btn_width')
			self.header_theme_btn_height = self._config.getint('header', 'theme_btn_height')
			self.header_theme_btn_radius = self._config.getint('header', 'theme_btn_radius')
			self.header_theme_btn_offset = self._config.getint('header', 'theme_btn_offset')
		else:
			logging.critical('Секция "header" не найдена')
		
		if 'footer' in self._config:
			self.footer_height = self._config.getint('footer', 'height')
			self.footer_padding = self._config.getint('footer', 'padding')
			self.footer_language_btn_width = self._config.getint('footer', 'language_btn_width')
			self.footer_language_btn_height = self._config.getint('footer', 'language_btn_height')
			self.footer_language_btn_radius = self._config.getint('footer', 'language_btn_radius')
			self.footer_language_btn_offset = self._config.getint('footer', 'language_btn_offset')
		else:
			logging.critical('Секция "footer" не найдена')

		if 'main_menu' in self._config:
			self.main_menu_margin = self._config.getint('main_menu', 'margin')
			self.main_menu_scroll_spacing = self._config.getint('main_menu', 'scroll_spacing')
			self.main_menu_swipe_width = self._config.getint('main_menu', 'swipe_width')
			self.main_menu_swipe_radius = self._config.getint('main_menu', 'swipe_radius')
			self.main_menu_swipe_spacing = self._config.getint('main_menu', 'swipe_spacing')
		else:
			logging.critical('Секция "main_menu" не найдена')
