import os
import logging
import weakref
from typing import Callable
from configparser import ConfigParser, ExtendedInterpolation
from PyQt6.QtGui import QFontDatabase, QFont, QFontMetrics
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.enum import ColorName, FontName, FilterState
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Clr():
	_current_theme_id: int = 0
	all_theme: list[dict[ColorName, str]] = [{}, {}, {}]
	filter_field: dict[FilterState, str] = {}

	_subscribers: set[weakref.WeakMethod] = set()

	@classmethod
	def get_theme_id(cls) -> int:
		return cls._current_theme_id

	@classmethod
	def set_theme_id(cls, value: int):
		if cls._current_theme_id != value:
			cls._current_theme_id = value
			cls._notify_subscribers()

	@classmethod
	def subscribe(cls, callback: Callable[[], None]):
		if hasattr(callback, '__self__') and callback.__self__ is not None:
			weak_method = weakref.WeakMethod(callback)
			cls._subscribers.add(weak_method)

	@classmethod
	def _notify_subscribers(cls):
		dead_subscribers = set()

		for weak_method in cls._subscribers:
			callback = weak_method()
			if callback is not None:
				try:
					callback()
				except RuntimeError:
					dead_subscribers.add(weak_method)
			else:
				dead_subscribers.add(weak_method)

		cls._subscribers -= dead_subscribers


	@classmethod
	def main_bg(cls) -> str:
		return cls.all_theme[cls._current_theme_id][ColorName.MAIN_BACKGROUND]
	
	@classmethod
	def sub_bg(cls) -> str:
		return cls.all_theme[cls._current_theme_id][ColorName.SUB_BACKGROUND]

	@classmethod
	def accent_bg(cls) -> str:
		return cls.all_theme[cls._current_theme_id][ColorName.ACCENT_BACKGROUND]
	
	@classmethod
	def main_brd(cls) -> str:
		return cls.all_theme[cls._current_theme_id][ColorName.MAIN_BORDER]

	@classmethod
	def font(cls) -> str:
		return cls.all_theme[cls._current_theme_id][ColorName.FONT]

	@classmethod
	def filter_bg(cls, state: FilterState) -> str:
		return cls.filter_field[state]
	
class Fnt():
	all_font: dict = {}

	@classmethod
	def shantell_sans(cls, font_size: int = 24) -> QFont:
		font_size = MathScripts.coordinate_scaling(font_size)[0]
		font = QFont(cls.all_font[FontName.SHANTELL_SANS], font_size)
		font.setFamilies([cls.all_font[FontName.SHANTELL_SANS], "SansSerif", "Arial"])
		font.setWeight(QFont.Weight.Medium)
		return font

	@classmethod
	def px_size(cls, font: QFont, text: str) -> tuple[int, int]:
		font_metrics = QFontMetrics(font)
		return font_metrics.horizontalAdvance(text), font_metrics.height()

class Theme(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Theme": Инициализация...')
		file_path = Path().theme_path
		self.font_dir_path = Path().font_dir_path

		Clr.set_theme_id(Setting().theme_id)
		self._config = ConfigParser(interpolation=ExtendedInterpolation())
		self._config.read(file_path, encoding='utf-8')

		self._read_conf()
		self._generate_font()
		logging.info('Модуль "Theme": Инициализация завершена')

	def _read_conf(self):
		if 'font_styles' in self._config:
			self._f_shantell_sans = self._config.get('font_styles', 'shantell_sans')
		else:
			logging.critical('Секция "font_styles" не найдена')
			
		if 'other' in self._config:
			Clr.filter_field[FilterState.NEUTRAL] = self._config.get('other', 'filter_neutral_background_color')
			Clr.filter_field[FilterState.DISABLE] = self._config.get('other', 'filter_disable_background_color')
			Clr.filter_field[FilterState.ENABLE] = self._config.get('other', 'filter_enable_background_color')
		else:
			logging.critical('Секция "other" не найдена')

		if 'blue' in self._config:
			Clr.all_theme[0][ColorName.MAIN_BACKGROUND] = self._config.get('blue', 'main_background_color')
			Clr.all_theme[0][ColorName.SUB_BACKGROUND] = self._config.get('blue', 'sub_background_color')
			Clr.all_theme[0][ColorName.ACCENT_BACKGROUND] = self._config.get('blue', 'accent_background_color')
			Clr.all_theme[0][ColorName.MAIN_BORDER] = self._config.get('blue', 'main_border_color')
			Clr.all_theme[0][ColorName.FONT] = self._config.get('blue', 'font_color')
		else:
			logging.critical('Секция "green" не найдена')
		
		if 'green' in self._config:
			Clr.all_theme[1][ColorName.MAIN_BACKGROUND] = self._config.get('green', 'main_background_color')
			Clr.all_theme[1][ColorName.SUB_BACKGROUND] = self._config.get('green', 'sub_background_color')
			Clr.all_theme[1][ColorName.ACCENT_BACKGROUND] = self._config.get('green', 'accent_background_color')
			Clr.all_theme[1][ColorName.MAIN_BORDER] = self._config.get('green', 'main_border_color')
			Clr.all_theme[1][ColorName.FONT] = self._config.get('green', 'font_color')
		else:
			logging.critical('Секция "red" не найдена')
		
		if 'red' in self._config:
			Clr.all_theme[2][ColorName.MAIN_BACKGROUND] = self._config.get('red', 'main_background_color')
			Clr.all_theme[2][ColorName.SUB_BACKGROUND] = self._config.get('red', 'sub_background_color')
			Clr.all_theme[2][ColorName.ACCENT_BACKGROUND] = self._config.get('red', 'accent_background_color')
			Clr.all_theme[2][ColorName.MAIN_BORDER] = self._config.get('red', 'main_border_color')
			Clr.all_theme[2][ColorName.FONT] = self._config.get('red', 'font_color')
		else:
			logging.critical('Секция "blue" не найдена')

	def _generate_font(self):
		Fnt.all_font[FontName.SHANTELL_SANS] = self._generate_ShantellSans()

	def _generate_ShantellSans(self) -> str:
		font_path = os.path.abspath(f'{self.font_dir_path}/{self._f_shantell_sans}/ShantellSans-Medium.ttf')

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
