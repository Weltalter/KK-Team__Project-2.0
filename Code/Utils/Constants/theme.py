import os
import logging
from configparser import ConfigParser, ExtendedInterpolation
from PyQt6.QtGui import QFontDatabase, QFont
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Theme(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Инициализация данных Theme...')
		file_path = Path().theme_path
		self.font_dir_path = Path().font_dir_path

		self.__current_theme = Setting().theme
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Инициализация завершена')

	def __read_conf(self):
		if 'font_styles' in self.__config:
			self.__shantell_sans = self.__config.get('font_styles', 'shantell_sans')
		else:
			logging.critical('Секция "font_styles" не найдена')

		if self.__current_theme in self.__config:
			self.main_background_color = self.__config.get(self.__current_theme, 'main_background_color')
			self.sub_background_color = self.__config.get(self.__current_theme, 'sub_background_color')
			self.accent_background_color = self.__config.get(self.__current_theme, 'accent_background_color')
			self.main_border_color = self.__config.get(self.__current_theme, 'main_border_color')
			self.font_color = self.__config.get(self.__current_theme, 'font_color')
		else:
			logging.critical(f'Секция "{self.__current_theme}" не найдена')

	def get_main_font(self, font_size: int = 24) -> QFont:
		font_size = MathScripts.coordinate_scaling(font_size)[0]
		font_path = os.path.abspath(f'{self.font_dir_path}/{self.__shantell_sans}/ShantellSans-Medium.ttf')

		if not os.path.exists(font_path):
			logging.error(f'Файл шрифта не найден по пути: {font_path}')
			logging.info('Применен стандартный QFont')
			return QFont('SansSerif', 11)

		font_id = QFontDatabase.addApplicationFont(font_path)

		if font_id == -1:
			logging.error(f'Файл шрифта поврежден или имеет неверный формат: {font_path}')
			logging.info('Применен стандартный QFont')
			return QFont('SansSerif', 11)

		font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
		
		font = QFont(font_family, font_size)
		font.setFamilies([font_family, "Arial", "SansSerif"])
		font.setWeight(QFont.Weight.Medium)
		logging.info(f'Шрифт {font_family} успешно загружен')
		return font
