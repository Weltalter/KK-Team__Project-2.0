from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
	QPushButton,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
	QScrollArea,
	QScroller,
	QScrollerProperties,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Theme
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.theme_dropdown import ThemeDropdown
from Code.UI.Component.main_menu_scroll_area import MainMenuScrollArea


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.theme = Theme()
		self.setWindowFlags( Qt.WindowType.FramelessWindowHint)

		self.setGeometry(*MathScripts.coordinate_scaling(250, 100, 1600, 800))
		self.setCentralWidget(self.build_window())

	def build_window(self) -> QWidget:
		central_widget = QWidget()
		main_layout = QHBoxLayout(central_widget)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		#region СЕКТОР 1: Боковое меню (Sidebar)
		sidebar_widget = QWidget()
		sidebar_widget.setObjectName("Sidebar")
		sidebar_widget.setStyleSheet(f"background-color: {self.theme.sub_background_color};")
		sidebar_widget.setFixedWidth(*MathScripts.coordinate_scaling(120))

		btn_setting = IconButton(path_to_icon="./DataFile/Files.img/temp files/settings.svg", parent=sidebar_widget)
		#btn_setting.clicked.connect(self.close)
		btn_setting.setGeometry(*MathScripts.coordinate_scaling(20, 20, 80, 80))
		
		btn_export = IconButton(path_to_icon="./DataFile/Files.img/temp files/upload-3.svg", parent=sidebar_widget)
		#btn_export.clicked.connect(self.close)
		btn_export.setGeometry(*MathScripts.coordinate_scaling(20, 120, 80, 80))
		
		btn_import = IconButton(path_to_icon="./DataFile/Files.img/temp files/download-8.svg", parent=sidebar_widget)
		#btn_import.clicked.connect(self.close)
		btn_import.setGeometry(*MathScripts.coordinate_scaling(20, 220, 80, 80))
		
		btn_close = IconButton(path_to_icon="./DataFile/Files.img/temp files/create-note.svg", parent=sidebar_widget)
		btn_close.clicked.connect(self.close)
		btn_close.setGeometry(*MathScripts.coordinate_scaling(20, 700, 80, 80))
		
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
		header_widget.setStyleSheet(f"background-color: {self.theme.main_background_color};") 
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
		content_widget.setStyleSheet(f"background-color: {self.theme.main_background_color};")

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
		footer_widget.setStyleSheet(f"background-color: {self.theme.main_background_color};") 
		footer_widget.setFixedHeight(*MathScripts.coordinate_scaling(40))

		footer_layout = QVBoxLayout(footer_widget)

		creator_lbl = QLabel("Версия и создатели")
		creator_lbl.setFont(self.theme.get_main_font(14))
		creator_lbl.setStyleSheet(f"QLabel {{ color: {self.theme.font_color}; }}")
		footer_layout.addWidget(creator_lbl, alignment=Qt.AlignmentFlag.AlignRight)
		
		body_layout.addWidget(footer_widget)
		#endregion

		main_layout.addLayout(body_layout)

		return central_widget
