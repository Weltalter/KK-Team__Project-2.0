import logging
from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
)
from PyQt6.QtCore import Qt
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.theme_dropdown import ThemeDropdown
from Code.UI.Component.language_dropdown import LanguageDropdown
from Code.UI.Component.main_menu_scroll_area import MainMenuScrollArea
from Code.UI.Component.main_sidebar import MainSidebar


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		logging.info('Экран "MainWindow": Инициализация...')
		self._coordinate = Coordinate()
		self._message = Message()
		self._icon = Icon()
		self.setWindowFlags( Qt.WindowType.FramelessWindowHint)

		self.setGeometry(*MathScripts.coordinate_scaling(
			self._coordinate.window_x,
			self._coordinate.window_y,
			self._coordinate.window_width,
			self._coordinate.window_height
		))
		self.setCentralWidget(self.build_window())
		logging.info('Экран "MainWindow": Инициализация завершена')

	def build_window(self) -> QWidget:
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		#region СЕКТОР 1: Боковое меню (Sidebar)
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

		#region ПРОМЕЖУТОЧНЫЙ LAYOUT (Для разделения на основной контент и низ)
		body_layout = QVBoxLayout()
		body_layout.setSpacing(0)
		body_layout.setContentsMargins(0, 0, 0, 0)
		#endregion

		#region СЕКТОР 2: Верхняя панель (Header)
		header_widget = QWidget()
		header_widget.setObjectName("Header")
		header_widget.setFixedHeight(*MathScripts.coordinate_scaling(self._coordinate.header_height)) 

		header_layout = QHBoxLayout(header_widget)
		
		padding = MathScripts.coordinate_scaling(self._coordinate.header_padding)[0]
		header_layout.setContentsMargins(padding, padding, padding, padding)
		header_layout.setSpacing(0)
		
		btn_theme = ThemeDropdown(parent=header_widget)

		header_layout.addStretch()
		header_layout.addWidget(btn_theme)
		
		body_layout.addWidget(header_widget)
		#endregion

		#region СЕКТОР 3: Главный контент (Main Content)
		content_widget = QWidget()
		content_widget.setObjectName("Content")

		content_layout = QHBoxLayout(content_widget)
		
		# ========================================================
		# 1. ЗАДАЕМ ОТСТУПЫ 40 ПИКСЕЛЕЙ ОТ КРАЕВ С УЧЕТОМ МАСШТАБА
		# ========================================================
		content_margin = MathScripts.coordinate_scaling(self._coordinate.main_menu_margin)[0]
		content_layout.setContentsMargins(content_margin, content_margin, content_margin, content_margin)
		content_layout.setSpacing(0)

		# Создаем QScrollArea (область прокрутки)
		mm_scroll_area_width = self.width() - sidebar_expand_w - 2*content_margin
		mm_scroll_area = MainMenuScrollArea(width=mm_scroll_area_width, parent=content_widget)
		#content_layout.addStretch()
		content_layout.addWidget(mm_scroll_area)
		
		body_layout.addWidget(content_widget)
		#endregion

		#region СЕКТОР 4: Нижняя панель (Footer)
		footer_widget = QWidget()
		footer_widget.setObjectName("Footer")
		footer_widget.setFixedHeight(*MathScripts.coordinate_scaling(self._coordinate.footer_height))

		footer_layout = QHBoxLayout(footer_widget)

		padding = MathScripts.coordinate_scaling(self._coordinate.footer_padding)[0]
		footer_layout.setContentsMargins(padding, padding, padding, padding)
		footer_layout.setSpacing(0)

		creator_lbl = QLabel(self._message.m_version)
		creator_lbl.setObjectName("VersionLabel")
		creator_lbl.setFont(Fnt.shantell_sans(14))
		
		btn_language = LanguageDropdown(parent=footer_widget)

		footer_layout.addWidget(btn_language)
		footer_layout.addStretch()
		footer_layout.addWidget(creator_lbl)

		body_layout.addWidget(footer_widget)
		#endregion

		main_layout.addLayout(body_layout)

		return central_widget

	def update_theme(self):
		self.setStyleSheet(f'''
			#Sidebar {{
				background-color: {Clr.sub_bg()};
			}}
			#Header {{
				background-color: {Clr.main_bg()};
			}}
			#Content {{
				background-color: {Clr.main_bg()};
			}}
			#Footer {{
				background-color: {Clr.main_bg()};
			}}
			#VersionLabel {{
				color: {Clr.font()};
			}}
		''')
	
	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
		Clr.subscribe(self.update_theme)
