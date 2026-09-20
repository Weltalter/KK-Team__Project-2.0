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
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.theme_dropdown import ThemeDropdown


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
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
		sidebar_widget.setStyleSheet("background-color: #606060;")
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
		header_widget.setStyleSheet("background-color: #1734cc;") 
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
		content_widget.setStyleSheet("background-color: #2ecc71;")

		content_layout = QHBoxLayout(content_widget)
		
		# ========================================================
		# 1. ЗАДАЕМ ОТСТУПЫ 40 ПИКСЕЛЕЙ ОТ КРАЕВ С УЧЕТОМ МАСШТАБА
		# ========================================================
		margin_40 = MathScripts.coordinate_scaling(40)[0]
		content_layout.setContentsMargins(margin_40, margin_40, margin_40, margin_40)
		content_layout.setSpacing(0)

		# Создаем QScrollArea (область прокрутки)
		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		
		scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

		scroll_content = QWidget()
		scroll_content.setStyleSheet("background-color: transparent;")

		# Внутренние отступы самого скролла сбрасываем в 0, 
		# так как внешние 40 пикселей мы уже настроили в content_layout
		scroll_layout = QHBoxLayout(scroll_content)
		scroll_layout.setContentsMargins(0, 0, 0, 0)
		scroll_layout.setSpacing(15)

		btn_w, btn_h = MathScripts.coordinate_scaling(265, 600)

		for i in range(1, 8):
			btn = IconButton(path_to_icon="./DataFile/Files.img/temp files/right-square.svg")
			btn.clicked.connect(lambda checked, num=i: print(f"Клик по кнопке {num}!"))
			btn.setFixedSize(btn_w, btn_h)
			scroll_layout.addWidget(btn)

		scroll_area.setWidget(scroll_content)

		# Высоту скролла делаем строго равной высоте кнопок, 
		# так как отступы теперь контролируются внешним макетом
		scroll_area.setFixedHeight(btn_h)

		# --- НАСТРОЙКА ИНТЕНСИВНОСТИ (ФИЗИКИ) ---
		QScroller.grabGesture(
			scroll_area.viewport(), 
			QScroller.ScrollerGestureType.LeftMouseButtonGesture
		)
		scroller = QScroller.scroller(scroll_area.viewport())
		props = QScrollerProperties()
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumVelocity, 0.15)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.DecelerationFactor, 0.25)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, 0.5)
		scroller.setScrollerProperties(props)

		# ========================================================
		# 2. УБИРАЕМ ALIGNMENT, ЧТОБЫ СКРОЛЛ РАСТЯНУЛСЯ ПО ШИРИНЕ
		# ========================================================
		content_layout.addWidget(scroll_area)
		
		body_layout.addWidget(content_widget)
		#endregion

		#region СЕКТОР 4: Нижняя панель (Footer)
		footer_widget = QWidget()
		footer_widget.setObjectName("Footer")
		footer_widget.setStyleSheet("background-color: #e74c3c;") 
		footer_widget.setFixedHeight(*MathScripts.coordinate_scaling(40))

		footer_layout = QVBoxLayout(footer_widget)
		footer_layout.addWidget(QLabel("Версия и создатели"), alignment=Qt.AlignmentFlag.AlignRight)
		
		body_layout.addWidget(footer_widget)
		#endregion

		main_layout.addLayout(body_layout)

		return central_widget
