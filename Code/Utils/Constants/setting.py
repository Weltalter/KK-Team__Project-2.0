import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Patterns.property_tracker import PropertyTracker
from Code.Utils.Constants.path import Path


class Setting(PropertyTracker, metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Setting": Инициализация...')
		file_path = Path().setting_path
		self._config = ConfigParser(interpolation=ExtendedInterpolation())
		self._config.read(file_path, encoding='utf-8')

		self._read_conf()
		logging.info('Модуль "Setting": Инициализация завершена')

	def _read_conf(self):
		if 'current' in self._config:
			self.theme_id = self._config.getint('current', 'theme_id')
			self.theme_title = self._config.get('current', 'theme_title')
			self.language_id = self._config.getint('current', 'language_id')
			self.language_title = self._config.get('current', 'language_title')
			self.maximum_velocity = self._config.getfloat('current', 'maximum_velocity', fallback=0.15)
			self.deceleration_factor = self._config.getfloat('current', 'deceleration_factor', fallback=0.25)
			self.mouse_press_event_delay = self._config.getfloat('current', 'mouse_press_event_delay', fallback=0.5)
			self.hover_pixmap_brightness = self._config.getfloat('current', 'hover_pixmap_brightness', fallback=0.85)
			self.pressed_pixmap_brightness = self._config.getfloat('current', 'pressed_pixmap_brightness', fallback=0.70)
			self.hover_color_brightness = self._config.getfloat('current', 'hover_color_brightness', fallback=0.85)
			self.pressed_color_brightness = self._config.getfloat('current', 'pressed_color_brightness', fallback=0.70)
		else:
			logging.critical('Секция "current" не найдена')

	def save_conf(self):
		if not getattr(self, 'is_changed', False):
			logging.info('Модуль "Setting": Изменений нет, перезапись файла отменена')
			return

		logging.info('Модуль "Setting": Обнаружены изменения, сохранение в файл...')

		if 'current' not in self._config:
			self._config.add_section('current')

		self._config.set('current', 'theme_id', str(self.theme_id))
		self._config.set('current', 'theme_title', str(self.theme_title))
		self._config.set('current', 'language_id', str(self.language_id))
		self._config.set('current', 'language_title', str(self.language_title))
		self._config.set('current', 'maximum_velocity', str(self.maximum_velocity))
		self._config.set('current', 'deceleration_factor', str(self.deceleration_factor))
		self._config.set('current', 'mouse_press_event_delay', str(self.mouse_press_event_delay))
		self._config.set('current', 'hover_pixmap_brightness', str(self.hover_pixmap_brightness))
		self._config.set('current', 'pressed_pixmap_brightness', str(self.pressed_pixmap_brightness))

		file_path = Path().setting_path
		try:
			with open(file_path, 'w', encoding='utf-8') as configfile:
				self._config.write(configfile)
			
			logging.info(f'Модуль "Setting": Данные успешно перезаписаны в {file_path}')
			
			super().__setattr__('is_changed', False)
			
		except Exception as e:
			logging.error(f'Модуль "Setting": Не удалось сохранить файл конфигурации')