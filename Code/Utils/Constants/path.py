import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton


class Path(metaclass=MetaSingleton):
	path: str = 'DataFile/Files.ini/path.ini'
	def __init__(self):
		logging.info('Модуль "Path": Инициализация...')
		self._config = ConfigParser(interpolation=ExtendedInterpolation())
		self._config.read(self.path, encoding='utf-8')

		self._read_conf()
		logging.info('Модуль "Path": Инициализация завершена')


	def _read_conf(self):
		if 'files' in self._config:
			self.coordinate_path = self._config.get('files', 'coordinate_file')
			self.language_path = self._config.get('files', 'language_file')
			self.setting_path = self._config.get('files', 'setting_file')
			self.theme_path = self._config.get('files', 'theme_file')
			self.icon_path = self._config.get('files', 'icon_file')
		else:
			logging.critical('Секция "files" не найдена')
		
		self.font_dir_path = self._config.get('DEFAULT', 'main_font_dir')
