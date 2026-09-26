from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton


class Path(metaclass=MetaSingleton):
	path: str = 'DataFile/Files.ini/path.ini'
	def __init__(self):
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(self.path, encoding='utf-8')

		self.__read_conf()

	def __read_conf(self):
		if 'dir' in self.__config:
			self.coordinate_path = self.__config.get('dir', 'coordinate_dir')
			self.language_path = self.__config.get('dir', 'language_dir')

		if 'files' in self.__config:
			self.setting_path = self.__config.get('files', 'setting_file')
			self.theme_path = self.__config.get('files', 'theme_file')
		
		self.font_dir_path = self.__config.get('DEFAULT', 'main_font_dir')
