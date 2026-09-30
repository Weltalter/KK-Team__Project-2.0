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
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.theme_dropdown import ThemeDropdown
from Code.UI.Component.language_dropdown import LanguageDropdown
from Code.UI.Component.main_menu_scroll_area import MainMenuScrollArea


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		logging.info('Экран "MainWindow": Инициализация...')
		self.__coordinate = Coordinate()
		self.__theme = Theme()
		self.__message = Message()
		self.__icon = Icon()
		self.setWindowFlags( Qt.WindowType.FramelessWindowHint)

		self.setGeometry(*MathScripts.coordinate_scaling(
			self.__coordinate.window_x,
			self.__coordinate.window_y,
			self.__coordinate.window_width,
			self.__coordinate.window_height
		))
		self.setCentralWidget(self.build_window())
		logging.info('Экран "MainWindow": Инициализация завершена')

	def build_window(self) -> QWidget:
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		#region СЕКТОР 1: Боковое меню (Sidebar)
		sidebar_widget = QWidget()
		sidebar_widget.setObjectName("Sidebar")
		sidebar_widget.setStyleSheet(f"background-color: {self.__theme.sub_background_color};")
		sidebar_widget.setFixedWidth(*MathScripts.coordinate_scaling(self.__coordinate.sidebar_width))

		size = MathScripts.coordinate_scaling(self.__coordinate.sidebar_btn_size)[0]
		btn_setting = IconButton(width=size, height=size, path_to_icon=self.__icon.i_setting, parent=sidebar_widget)
		btn_setting.move(*MathScripts.coordinate_scaling(self.__coordinate.sidebar_btn_x, self.__coordinate.sidebar_setting_btn_y))
		
		btn_export = IconButton(width=size, height=size, path_to_icon=self.__icon.i_export, parent=sidebar_widget)
		btn_export.move(*MathScripts.coordinate_scaling(self.__coordinate.sidebar_btn_x, self.__coordinate.sidebar_export_btn_y))
		
		btn_import = IconButton(width=size, height=size, path_to_icon=self.__icon.i_import, parent=sidebar_widget)
		btn_import.move(*MathScripts.coordinate_scaling(self.__coordinate.sidebar_btn_x, self.__coordinate.sidebar_import_btn_y))
		
		btn_close = IconButton(width=size, height=size, path_to_icon=self.__icon.i_exit, parent=sidebar_widget)
		btn_close.move(*MathScripts.coordinate_scaling(self.__coordinate.sidebar_btn_x, self.__coordinate.sidebar_exit_btn_y))
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
		header_widget.setFixedHeight(*MathScripts.coordinate_scaling(self.__coordinate.header_height)) 

		header_layout = QHBoxLayout(header_widget)
		
		padding = MathScripts.coordinate_scaling(self.__coordinate.header_padding)[0]
		header_layout.setContentsMargins(padding, padding, padding, padding)
		header_layout.setSpacing(0)

		btn_theme = ThemeDropdown(size=MathScripts.coordinate_scaling(self.__coordinate.header_theme_btn_size)[0])

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
		content_margin = MathScripts.coordinate_scaling(self.__coordinate.main_menu_margin)[0]
		content_layout.setContentsMargins(content_margin, content_margin, content_margin, content_margin)
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
		footer_widget.setFixedHeight(*MathScripts.coordinate_scaling(self.__coordinate.footer_height))

		footer_layout = QHBoxLayout(footer_widget)

		padding = MathScripts.coordinate_scaling(self.__coordinate.footer_padding)[0]
		footer_layout.setContentsMargins(padding, padding, padding, padding)
		footer_layout.setSpacing(0)

		creator_lbl = QLabel(self.__message.m_version)
		creator_lbl.setFont(self.__theme.get_shantell_sans(14))
		creator_lbl.setStyleSheet(f"QLabel {{ color: {self.__theme.font_color}; }}")
		
		btn_theme1 = LanguageDropdown(width=120, height=35, radius=10)

		footer_layout.addWidget(btn_theme1)
		footer_layout.addStretch()
		footer_layout.addWidget(creator_lbl)

		body_layout.addWidget(footer_widget)
		#endregion

		main_layout.addLayout(body_layout)

		return central_widget
