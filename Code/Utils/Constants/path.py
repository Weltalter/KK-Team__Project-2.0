from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton


class Path(metaclass=MetaSingleton):
	path: str = 'DataFile/Files.ini/path.ini'
	def __init__(self):
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(self.path, encoding='utf-8')

		self.__read_conf()

	def __read_conf(self):
		if 'dir_ini' in self.__config:
			self.coordinate_path = self.__config.get('dir_ini', 'coordinate_dir')
			self.language_path = self.__config.get('dir_ini', 'language_dir')

		if 'files_ini' in self.__config:
			self.setting_path = self.__config.get('files_ini', 'setting_file')
			self.theme_path = self.__config.get('files_ini', 'theme_file')
