import logging
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.UI.main_window import MainWindow
from Code.Utils.Constants.path import Path
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.Utils.logger import Logger
from Code.Utils.libraries import (
	ApplicationLibrary,
	BookLibrary,
	GameLibrary,
	MedicineLibrary,
	MovieLibrary,
	RecipeLibrary,
	WebsiteLibrary
)


class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		self.__initialize()

	def __initialize(self):
		Logger.initialize()
		
		logging.info('RT: Инициализация классов доступа...')
		self.__path = Path()
		self.__setting = Setting()
		self.__coordinate = Coordinate()
		self.__theme = Theme()
		self.__message = Message()
		self.__icon = Icon()
		logging.info('RT: Инициализация классов доступа завершена')

		logging.info('RT: Инициализация библиотек...')
		self.__l_application = ApplicationLibrary()
		self.__l_application.import_data()

		self.__l_book = BookLibrary()
		self.__l_book.import_data()

		self.__l_game = GameLibrary()
		self.__l_game.import_data()

		self.__l_medicine = MedicineLibrary()
		self.__l_medicine.import_data()

		self.__l_movie = MovieLibrary()
		self.__l_movie.import_data()

		self.__l_recipe = RecipeLibrary()
		self.__l_recipe.import_data()

		self.__l_website = WebsiteLibrary()
		self.__l_website.import_data()
		logging.info('RT: Инициализация библиотек завершена')

	def run(self):
		self.test = MainWindow()
		self.test.show()

	def before_exit(self):
		logging.info('RT: Завершение работы...')
		logging.info('RT: Сохранение данных...')
		
		self.__setting.save_conf()
		logging.info('RT: Настройки сохранены')

		self.__l_application.export_data()
		self.__l_book.export_data()
		self.__l_game.export_data()
		self.__l_medicine.export_data()
		self.__l_movie.export_data()
		self.__l_recipe.export_data()
		self.__l_website.export_data()
		logging.info('RT: библиотеки сохранены')
