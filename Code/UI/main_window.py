import logging
from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.theme_dropdown import ThemeDropdown
from Code.UI.Component.main_menu_scroll_area import MainMenuScrollArea


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		logging.info('Инициализация экрана "MainWindow"...')
		self.__theme = Theme()
		self.__message = Message()
		self.__icon = Icon()
		self.setWindowFlags( Qt.WindowType.FramelessWindowHint)

		self.setGeometry(*MathScripts.coordinate_scaling(250, 100, 1600, 800))
		self.setCentralWidget(self.build_window())
		logging.info('Инициализация экрана "MainWindow" завершена')

	def build_window(self) -> QWidget:
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		#region СЕКТОР 1: Боковое меню (Sidebar)
		sidebar_widget = QWidget()
		sidebar_widget.setObjectName("Sidebar")
		sidebar_widget.setStyleSheet(f"background-color: {self.__theme.sub_background_color};")
		sidebar_widget.setFixedWidth(*MathScripts.coordinate_scaling(80))

		size = MathScripts.coordinate_scaling(40)[0]
		btn_setting = IconButton(width=size, height=size, path_to_icon=self.__icon.i_setting, parent=sidebar_widget)
		btn_setting.move(*MathScripts.coordinate_scaling(20, 20))
		
		btn_export = IconButton(width=size, height=size, path_to_icon=self.__icon.i_export, parent=sidebar_widget)
		btn_export.move(*MathScripts.coordinate_scaling(20, 80))
		
		btn_import = IconButton(width=size, height=size, path_to_icon=self.__icon.i_import, parent=sidebar_widget)
		btn_import.move(*MathScripts.coordinate_scaling(20, 140))
		
		btn_close = IconButton(width=size, height=size, path_to_icon=self.__icon.i_exit, parent=sidebar_widget)
		btn_close.move(*MathScripts.coordinate_scaling(20, 740))
		btn_close.clicked.connect(self.close)
		
		main_layout.addWidget(sidebar_widget)
		#endregion

		#region ПРОМЕЖУТОЧНЫЙ LAYOUT (Для разделения на основной контент и низ)
		body_layout = QVBoxLayout()
		body_layout.setSpacing(0)
		body_layout.setContentsMargins(0, 0, 0, 0)
		#endregion

		#region СЕКТОР 2: Верхняя панель (Header)
		header_widget = QWidget()
		header_widget.setObjectName("Header")
		header_widget.setStyleSheet(f"background-color: {self.__theme.main_background_color};") 
		header_widget.setFixedHeight(*MathScripts.coordinate_scaling(60)) 

		header_layout = QHBoxLayout(header_widget)
		
		padding = MathScripts.coordinate_scaling(10)[0]
		header_layout.setContentsMargins(padding, padding, padding, padding)
		header_layout.setSpacing(0)

		scaled_size = MathScripts.coordinate_scaling(40)[0]
		btn_theme = ThemeDropdown(size=scaled_size)

		header_layout.addStretch()
		header_layout.addWidget(btn_theme)
		
		body_layout.addWidget(header_widget)
		#endregion

		#region СЕКТОР 3: Главный контент (Main Content)
		content_widget = QWidget()
		content_widget.setObjectName("Content")
		content_widget.setStyleSheet(f"background-color: {self.__theme.main_background_color};")

		content_layout = QHBoxLayout(content_widget)
		
		# ========================================================
		# 1. ЗАДАЕМ ОТСТУПЫ 40 ПИКСЕЛЕЙ ОТ КРАЕВ С УЧЕТОМ МАСШТАБА
		# ========================================================
		content_layout.setContentsMargins(*MathScripts.coordinate_scaling(40, 40, 40, 40))
		content_layout.setSpacing(0)

		# Создаем QScrollArea (область прокрутки)
		mm_scroll_area = MainMenuScrollArea(parent=content_widget)
		content_layout.addWidget(mm_scroll_area)
		
		body_layout.addWidget(content_widget)
		#endregion

		#region СЕКТОР 4: Нижняя панель (Footer)
		footer_widget = QWidget()
		footer_widget.setObjectName("Footer")
		footer_widget.setStyleSheet(f"background-color: {self.__theme.main_background_color};") 
		footer_widget.setFixedHeight(*MathScripts.coordinate_scaling(40))

		footer_layout = QVBoxLayout(footer_widget)

		creator_lbl = QLabel(self.__message.version)
		creator_lbl.setFont(self.__theme.get_main_font(14))
		creator_lbl.setStyleSheet(f"QLabel {{ color: {self.__theme.font_color}; }}")
		footer_layout.addWidget(creator_lbl, alignment=Qt.AlignmentFlag.AlignRight)
		
		body_layout.addWidget(footer_widget)
		#endregion

		main_layout.addLayout(body_layout)

		return central_widget
