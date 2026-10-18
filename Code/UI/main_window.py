import logging
from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
	QHBoxLayout
)
from PyQt6.QtCore import Qt
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.Utils.Constants.enum import MenuId
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.main_sidebar import MainSidebar
from Code.UI.Menu.menu_manager import MenuManager


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		logging.info('Экран "MainWindow": Инициализация...')
		self._coordinate = Coordinate()
		self._message = Message()
		self._icon = Icon()
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

		self.setGeometry(*MathScripts.coordinate_scaling(
			self._coordinate.window_x,
			self._coordinate.window_y,
			self._coordinate.window_width,
			self._coordinate.window_height
		))
		self._menu_manager = MenuManager()
		self._menu_manager.set_screen_geometry(self.geometry())
		self._menu_manager.build_menu()
		self.setCentralWidget(self.build_window())
		logging.info('Экран "MainWindow": Инициализация завершена')

	def build_window(self) -> QWidget:
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		#region Боковое меню (Sidebar)
		sidebar_collaps_w, sidebar_expand_w = MathScripts.coordinate_scaling(self._coordinate.sidebar_collapsed_width, self._coordinate.sidebar_expanded_width)
		sidebar_widget = MainSidebar(collaps_width=sidebar_collaps_w, expand_width=sidebar_expand_w)
		sidebar_widget.setObjectName("Sidebar")

		size = MathScripts.coordinate_scaling(self._coordinate.sidebar_btn_size)[0]
		btn_setting = IconButton(width=size, height=size, path_to_icon=self._icon.i_setting, parent=sidebar_widget)
		btn_setting.move(*MathScripts.coordinate_scaling(self._coordinate.sidebar_btn_x, self._coordinate.sidebar_setting_btn_y))
		
		btn_export = IconButton(width=size, height=size, path_to_icon=self._icon.i_export, parent=sidebar_widget)
		btn_export.move(*MathScripts.coordinate_scaling(self._coordinate.sidebar_btn_x, self._coordinate.sidebar_export_btn_y))
		
		btn_import = IconButton(width=size, height=size, path_to_icon=self._icon.i_import, parent=sidebar_widget)
		btn_import.move(*MathScripts.coordinate_scaling(self._coordinate.sidebar_btn_x, self._coordinate.sidebar_import_btn_y))
		
		btn_close = IconButton(width=size, height=size, path_to_icon=self._icon.i_exit, parent=sidebar_widget)
		btn_close.move(*MathScripts.coordinate_scaling(self._coordinate.sidebar_btn_x, self._coordinate.sidebar_exit_btn_y))
		btn_close.clicked.connect(self.close)
		
		main_layout.addWidget(sidebar_widget)
		#endregion

		main_layout.addWidget(self._menu_manager.widget, stretch=1)

		btn_setting.clicked.connect(lambda: self._menu_manager.switch_menu(MenuId.MAIN))
		return central_widget

	def update_theme(self):
		self.setStyleSheet(f'''
			#Sidebar {{
				background-color: {Clr.sub_bg()};
			}}
		''')
	
	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
		Clr.subscribe(self.update_theme)
