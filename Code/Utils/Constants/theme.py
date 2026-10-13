import os
import logging
from configparser import ConfigParser, ExtendedInterpolation
from PyQt6.QtGui import QFontDatabase, QFont
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.enum import ColorName, FontName
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Clr():
	current_theme_id: int
	all_theme: list[dict] = [{}, {}, {}]

	@staticmethod
	def main_bg() -> str:
		return Clr.all_theme[Clr.current_theme_id][ColorName.MAIN_BACKGROUND]
	
	@staticmethod
	def sub_bg() -> str:
		return Clr.all_theme[Clr.current_theme_id][ColorName.SUB_BACKGROUND]

	@staticmethod
	def accent_bg() -> str:
		return Clr.all_theme[Clr.current_theme_id][ColorName.ACCENT_BACKGROUND]
	
	@staticmethod
	def main_brd() -> str:
		return Clr.all_theme[Clr.current_theme_id][ColorName.MAIN_BORDER]

	@staticmethod
	def font() -> str:
		return Clr.all_theme[Clr.current_theme_id][ColorName.FONT]

class Fnt():
	all_font: dict = {}

	@staticmethod
	def shantell_sans(font_size: int = 24) -> QFont:
		font_size = MathScripts.coordinate_scaling(font_size)[0]
		font = QFont(Fnt.all_font[FontName.SHANTELL_SANS], font_size)
		font.setFamilies([Fnt.all_font[FontName.SHANTELL_SANS], "SansSerif", "Arial"])
		font.setWeight(QFont.Weight.Medium)
		return font

class Theme(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Theme": Инициализация...')
		file_path = Path().theme_path
		self.font_dir_path = Path().font_dir_path

		Clr.current_theme_id = Setting().theme_id
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		self.__generate_font()
		logging.info('Модуль "Theme": Инициализация завершена')

	def __read_conf(self):
		if 'font_styles' in self.__config:
			self.__f_shantell_sans = self.__config.get('font_styles', 'shantell_sans')
		else:
			logging.critical('Секция "font_styles" не найдена')

		if 'blue' in self.__config:
			Clr.all_theme[0][ColorName.MAIN_BACKGROUND] = self.__config.get('blue', 'main_background_color')
			Clr.all_theme[0][ColorName.SUB_BACKGROUND] = self.__config.get('blue', 'sub_background_color')
			Clr.all_theme[0][ColorName.ACCENT_BACKGROUND] = self.__config.get('blue', 'accent_background_color')
			Clr.all_theme[0][ColorName.MAIN_BORDER] = self.__config.get('blue', 'main_border_color')
			Clr.all_theme[0][ColorName.FONT] = self.__config.get('blue', 'font_color')
		else:
			logging.critical('Секция "green" не найдена')
		
		if 'green' in self.__config:
			Clr.all_theme[1][ColorName.MAIN_BACKGROUND] = self.__config.get('green', 'main_background_color')
			Clr.all_theme[1][ColorName.SUB_BACKGROUND] = self.__config.get('green', 'sub_background_color')
			Clr.all_theme[1][ColorName.ACCENT_BACKGROUND] = self.__config.get('green', 'accent_background_color')
			Clr.all_theme[1][ColorName.MAIN_BORDER] = self.__config.get('green', 'main_border_color')
			Clr.all_theme[1][ColorName.FONT] = self.__config.get('green', 'font_color')
		else:
			logging.critical('Секция "red" не найдена')
		
		if 'red' in self.__config:
			Clr.all_theme[2][ColorName.MAIN_BACKGROUND] = self.__config.get('red', 'main_background_color')
			Clr.all_theme[2][ColorName.SUB_BACKGROUND] = self.__config.get('red', 'sub_background_color')
			Clr.all_theme[2][ColorName.ACCENT_BACKGROUND] = self.__config.get('red', 'accent_background_color')
			Clr.all_theme[2][ColorName.MAIN_BORDER] = self.__config.get('red', 'main_border_color')
			Clr.all_theme[2][ColorName.FONT] = self.__config.get('red', 'font_color')
		else:
			logging.critical('Секция "blue" не найдена')

	def __generate_font(self):
		Fnt.all_font[FontName.SHANTELL_SANS] = self.__generate_ShantellSans()

	def __generate_ShantellSans(self) -> str:
		font_path = os.path.abspath(f'{self.font_dir_path}/{self.__f_shantell_sans}/ShantellSans-Medium.ttf')

		if not os.path.exists(font_path):
			logging.error(f'Файл шрифта не найден по пути: {font_path}')
			return QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont).family()

		font_id = QFontDatabase.addApplicationFont(font_path)

		if font_id == -1:
			logging.error(f'Файл шрифта поврежден или имеет неверный формат: {font_path}')
			return QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont).family()

		family = QFontDatabase.applicationFontFamilies(font_id)[0]
		logging.info(f'Шрифт {family} успешно загружен')
		return family
