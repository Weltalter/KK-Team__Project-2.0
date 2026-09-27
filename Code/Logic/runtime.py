import logging
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.libraries import *
from Code.UI.main_window import MainWindow
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.Utils.logger import Logger


class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		Logger.initialize()
		self.__path = Path()
		self.__setting = Setting()
		self.__theme = Theme()
		self.__message = Message()
		self.__icon = Icon()

	def run(self):
		self.test = MainWindow()
		self.test.show()

	def before_exit(self):
		logging.info('RT: Завершение работы...')
		logging.info('RT: Сохранение данных...')
		self.__setting.save_conf()
		logging.info('RT: Данные сохранены')
