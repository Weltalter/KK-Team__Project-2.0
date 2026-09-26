from configparser import ConfigParser, ExtendedInterpolation
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.path import Path


class Setting(metaclass=MetaSingleton):
	def __init__(self):
		file_path = Path().setting_path
		self.__config = ConfigParser(interpolation=ExtendedInterpolation())
		self.__config.read(file_path, encoding='utf-8')

		self.__read_conf()

	def __read_conf(self):
		if 'currect' in self.__config:
			self.theme = self.__config.get('currect', 'theme')
			self.language = self.__config.get('currect', 'language')
			self.MaximumVelocity = self.__config.getfloat('currect', 'MaximumVelocity', fallback=0.15)
			self.DecelerationFactor = self.__config.getfloat('currect', 'DecelerationFactor', fallback=0.25)
			self.MousePressEventDelay = self.__config.getfloat('currect', 'MousePressEventDelay', fallback=0.5)
