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
	WebsiteLibrary,
	AccountLibrary
)


class Runtime(metaclass=MetaSingleton):
	def __init__(self):
		self._initialize()

	def _initialize(self):
		Logger.initialize()
		
		logging.info('RT: Инициализация классов доступа...')
		self._path = Path()
		self._setting = Setting()
		self._coordinate = Coordinate()
		self._theme = Theme()
		self._message = Message()
		self._icon = Icon()
		logging.info('RT: Инициализация классов доступа завершена')

		logging.info('RT: Инициализация библиотек...')
		self._l_application = ApplicationLibrary()
		self._l_application.import_data()

		self._l_book = BookLibrary()
		self._l_book.import_data()

		self._l_game = GameLibrary()
		self._l_game.import_data()

		self._l_medicine = MedicineLibrary()
		self._l_medicine.import_data()

		self._l_movie = MovieLibrary()
		self._l_movie.import_data()

		self._l_recipe = RecipeLibrary()
		self._l_recipe.import_data()

		self._l_website = WebsiteLibrary()
		self._l_website.import_data()
		
		self._l_account = AccountLibrary()
		self._l_account.import_data()
		logging.info('RT: Инициализация библиотек завершена')

	def run(self):
		self.test = MainWindow()
		self.test.show()

	def before_exit(self):
		logging.info('RT: Завершение работы...')
		logging.info('RT: Сохранение данных...')
		
		self._setting.save_conf()
		logging.info('RT: Настройки сохранены')

		self._l_application.export_data()
		self._l_book.export_data()
		self._l_game.export_data()
		self._l_medicine.export_data()
		self._l_movie.export_data()
		self._l_recipe.export_data()
		self._l_website.export_data()
		self._l_account.export_data()
		logging.info('RT: библиотеки сохранены')
