from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting


class Message(metaclass=MetaSingleton):
	def __init__(self):
		file_path = Path().language_path

		self.__current_language = Setting().language
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(f'{file_path}/{self.__current_language}.ini', encoding='utf-8')

		self.__read_conf()

	def __read_conf(self):
		if 'main_menu' in self.__config:
			self.swipe_0 = self.__config.get('main_menu', 'swipe_0')
			self.swipe_1 = self.__config.get('main_menu', 'swipe_1')
			self.swipe_2 = self.__config.get('main_menu', 'swipe_2')
			self.swipe_3 = self.__config.get('main_menu', 'swipe_3')
			self.swipe_4 = self.__config.get('main_menu', 'swipe_4')
			self.swipe_5 = self.__config.get('main_menu', 'swipe_5')
			self.swipe_6 = self.__config.get('main_menu', 'swipe_6')
			self.swipe_7 = self.__config.get('main_menu', 'swipe_7')
			self.version = self.__config.get('main_menu', 'version')
