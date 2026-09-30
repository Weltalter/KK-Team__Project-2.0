import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Patterns.property_tracker import PropertyTracker
from Code.Utils.Constants.path import Path


class Setting(PropertyTracker, metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Setting": Инициализация...')
		file_path = Path().setting_path
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()
		logging.info('Модуль "Setting": Инициализация завершена')

	def __read_conf(self):
		if 'current' in self.__config:
			self.theme_id = self.__config.getint('current', 'theme_id')
			self.theme_title = self.__config.get('current', 'theme_title')
			self.language_id = self.__config.getint('current', 'language_id')
			self.language_title = self.__config.get('current', 'language_title')
			self.maximum_velocity = self.__config.getfloat('current', 'maximum_velocity', fallback=0.15)
			self.deceleration_factor = self.__config.getfloat('current', 'deceleration_factor', fallback=0.25)
			self.mouse_press_event_delay = self.__config.getfloat('current', 'mouse_press_event_delay', fallback=0.5)
			self.hover_pixmap_brightness = self.__config.getfloat('current', 'hover_pixmap_brightness', fallback=0.85)
			self.pressed_pixmap_brightness = self.__config.getfloat('current', 'pressed_pixmap_brightness', fallback=0.70)
			self.hover_color_brightness = self.__config.getfloat('current', 'hover_color_brightness', fallback=0.85)
			self.pressed_color_brightness = self.__config.getfloat('current', 'pressed_color_brightness', fallback=0.70)
		else:
			logging.critical('Секция "current" не найдена')

	def save_conf(self):
		if not getattr(self, 'is_changed', False):
			logging.info('Модуль "Setting": Изменений нет, перезапись файла отменена')
			return

		logging.info('Модуль "Setting": Обнаружены изменения, сохранение в файл...')

		if 'current' not in self.__config:
			self.__config.add_section('current')

		self.__config.set('current', 'theme_id', str(self.theme_id))
		self.__config.set('current', 'theme_title', str(self.theme_title))
		self.__config.set('current', 'language_id', str(self.language_id))
		self.__config.set('current', 'language_title', str(self.language_title))
		self.__config.set('current', 'maximum_velocity', str(self.maximum_velocity))
		self.__config.set('current', 'deceleration_factor', str(self.deceleration_factor))
		self.__config.set('current', 'mouse_press_event_delay', str(self.mouse_press_event_delay))
		self.__config.set('current', 'hover_pixmap_brightness', str(self.hover_pixmap_brightness))
		self.__config.set('current', 'pressed_pixmap_brightness', str(self.pressed_pixmap_brightness))

		file_path = Path().setting_path
		try:
			with open(file_path, 'w', encoding='utf-8') as configfile:
				self.__config.write(configfile)
			
			logging.info(f'Модуль "Setting": Данные успешно перезаписаны в {file_path}')
			
			super().__setattr__('is_changed', False)
			
		except Exception as e:
			logging.error(f'Модуль "Setting": Не удалось сохранить файл конфигурации')