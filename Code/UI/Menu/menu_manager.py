from PyQt6.QtWidgets import (
	QStackedWidget
)
from PyQt6.QtCore import QRect
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.Constants.enum import MenuId
from Code.UI.Menu.main_menu import MainMenu
from Code.UI.Menu.movie_menu import MovieMenu
from Code.UI.Menu.game_menu import GameMenu
from Code.UI.Menu.recipe_menu import RecipeMenu
from Code.UI.Menu.book_menu import BookMenu
from Code.UI.Menu.medicine_menu import MedicineMenu
from Code.UI.Menu.website_menu import WebsiteMenu
from Code.UI.Menu.application_menu import ApplicationMenu
from Code.UI.Menu.account_menu import AccountMenu


class MenuManager(metaclass=MetaSingleton):
	def __init__(self):
		self._screen_geometry: QRect = None
		self._current_menu_id: MenuId = MenuId.MAIN
		self._menu: dict = {}

		self.widget = QStackedWidget()

	def build_menu(self):
		self._menu = {
			MenuId.MAIN: MainMenu(self),
			MenuId.MOVIE: MovieMenu(self),
			MenuId.GAME: GameMenu(self),
			MenuId.RECIPE: RecipeMenu(self),
			MenuId.BOOK: BookMenu(self),
			MenuId.MEDICINE: MedicineMenu(self),
			MenuId.WEBSITE: WebsiteMenu(self),
			MenuId.APPLICATION: ApplicationMenu(self),
			MenuId.ACCOUNT: AccountMenu(self)
		}
		for menu_id, menu_widget in self._menu.items():
			self.widget.insertWidget(menu_id, menu_widget)
		self.widget.setCurrentIndex(self._current_menu_id)

	def switch_menu(self, menu_id: MenuId):
		if menu_id in self._menu:
			self._current_menu_id = menu_id
			self.widget.setCurrentIndex(menu_id)
	
	def set_screen_geometry(self, geometry: QRect):
		self._screen_geometry = geometry

	def get_screen_geometry(self) -> QRect:
		return self._screen_geometry
