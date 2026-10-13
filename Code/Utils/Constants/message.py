import logging
from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Message(metaclass=MetaSingleton):
	def __init__(self):
		logging.info('Модуль "Message": Инициализация...')
		file_path = Path().language_path

		self._current_language = Setting().language_title
		self._config = ConfigParser(interpolation=ExtendedInterpolation())
		self._config.read(file_path, encoding='utf-8')

		self._read_conf()
		logging.info('Модуль "Message": Инициализация завершена')

	def _read_conf(self):
		if 'language' in self._config:
			self.m_languages = [self._config.get('language', f'language_{i}') for i in range(len(self._config['language'].keys() - self._config['DEFAULT'].keys()))]

		if f'{self._current_language}.swipes' in self._config:
			self.m_swipes = [self._config.get(f'{self._current_language}.swipes', f'swipe_{i}') for i in range(len(self._config[f'{self._current_language}.swipes'].keys()))]
		else:
			logging.critical(f'Секция "{self._current_language}.swipes" не найдена')

		if f'{self._current_language}' in self._config:
			self.m_version = self._config.get(f'{self._current_language}', 'version')
		else:
			logging.critical(f'Секция "{self._current_language}" не найдена')
