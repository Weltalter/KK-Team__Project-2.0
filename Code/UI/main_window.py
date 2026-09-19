from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
	QPushButton,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from Code.Utils.Scripts.math_scripts import MathScripts


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowFlags(
			Qt.WindowType.FramelessWindowHint #| 
			#Qt.WindowType.WindowStaysOnTopHint
		)

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
		sidebar_widget.setStyleSheet("background-color: #3498db;")
		sidebar_widget.setFixedWidth(*MathScripts.coordinate_scaling(120))

		btn_setting = QPushButton("", sidebar_widget)
		#btn_setting.clicked.connect(self.close)
		btn_setting.setGeometry(*MathScripts.coordinate_scaling(20, 20, 80, 80))
		
		btn_export = QPushButton("", sidebar_widget)
		#btn_export.clicked.connect(self.close)
		btn_export.setGeometry(*MathScripts.coordinate_scaling(20, 120, 80, 80))
		
		btn_import = QPushButton("", sidebar_widget)
		#btn_import.clicked.connect(self.close)
		btn_import.setGeometry(*MathScripts.coordinate_scaling(20, 220, 80, 80))
		
		btn_close = QPushButton("", sidebar_widget)
		btn_close.clicked.connect(self.close)
		btn_close.setGeometry(*MathScripts.coordinate_scaling(20, 700, 80, 80))
		
		main_layout.addWidget(sidebar_widget)
		#endregion

		#region ПРОМЕЖУТОЧНЫЙ LAYOUT (Для разделения на основной контент и низ)
		body_layout = QVBoxLayout()
		body_layout.setSpacing(0)
		body_layout.setContentsMargins(0, 0, 0, 0)
		#endregion

		#region СЕКТОР 2: Главный контент (Main Content)
		content_widget = QWidget()
		content_widget.setObjectName("Content")
		content_widget.setStyleSheet("background-color: #2ecc71;")
		
		body_layout.addWidget(content_widget)
		#endregion

		#region СЕКТОР 3: Нижняя панель (Footer)
		header_widget = QWidget()
		header_widget.setObjectName("Header")
		header_widget.setStyleSheet("background-color: #e74c3c;") 
		header_widget.setFixedHeight(*MathScripts.coordinate_scaling(60)) 
		
		body_layout.addWidget(header_widget)
		#endregion

		main_layout.addLayout(body_layout)

		return central_widget
