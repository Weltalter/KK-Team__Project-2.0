import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path


class Setting(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Инициализация модуля Setting...')
		file_path = Path().setting_path
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Инициализация модуля Setting завершена')

	def __read_conf(self):
		if 'current' in self.__config:
			self.theme = self.__config.get('current', 'theme')
			self.language = self.__config.get('current', 'language')
			self.maximum_velocity = self.__config.getfloat('current', 'maximum_velocity', fallback=0.15)
			self.deceleration_factor = self.__config.getfloat('current', 'deceleration_factor', fallback=0.25)
			self.mouse_press_event_delay = self.__config.getfloat('current', 'mouse_press_event_delay', fallback=0.5)
			self.hover_pixmap_brightness = self.__config.getfloat('current', 'hover_pixmap_brightness', fallback=0.85)
			self.pressed_pixmap_brightness = self.__config.getfloat('current', 'pressed_pixmap_brightness', fallback=0.70)
		else:
			logging.critical('Секция "current" не найдена')
