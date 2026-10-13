import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Icon(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Icon": Инициализация...')
		file_path = Path().icon_path

		self._config = ConfigParser(interpolation=ExtendedInterpolation())
		self._config.read(f'{file_path}', encoding='utf-8')

		self._read_conf()
		logging.info('Модуль "Icon": Инициализация завершена')

	def _read_conf(self):
		if 'swipes' in self._config:
			self.i_swipes = [self._config.get('swipes', f'swipe_{i}') for i in range(len(self._config['swipes'].keys() - self._config['DEFAULT'].keys()))]
		else:
			logging.critical('Секция "swipes" не найдена')
		
		if 'sidebar' in self._config:
			self.i_setting = self._config.get('sidebar', 'setting')
			self.i_export = self._config.get('sidebar', 'export')
			self.i_import = self._config.get('sidebar', 'import')
			self.i_exit = self._config.get('sidebar', 'exit')
		else:
			logging.critical('Секция "sidebar" не найдена')
		
		if 'theme' in self._config:
			self.i_reload = self._config.get('theme', 'reload')
			self.i_themes = [self._config.get('theme', f'theme_{i}') for i in range(len(self._config['theme'].keys() - self._config['DEFAULT'].keys()) - 1)]
		else:
			logging.critical('Секция "theme" не найдена')
