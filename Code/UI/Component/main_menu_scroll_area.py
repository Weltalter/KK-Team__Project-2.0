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
	QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.UI.Component.icon_button import IconButton
from Code.UI.Component.rounded_icon_button import RoundedIconButton


class SwipeWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setStyleSheet("background-color: transparent;")
		
		self.layout = QVBoxLayout(parent)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(15)
	
	def set_button(self, width: int = 20, height: int = 20, radius: int = 10, path_to_icon="./DataFile/Files.img/ThemeIcons/reload.svg"):
		btn = RoundedIconButton(width=width, height=height, radius=radius, path_to_icon=path_to_icon)
		self.layout.addWidget(btn)

	def set_label(self, text: str = ''):
		lbl = QLabel(text)
		self.layout.addWidget(lbl)

class MainMenuScrollArea(QScrollArea):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setWidgetResizable(True)
		
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

		# --- НАСТРОЙКА ИНТЕНСИВНОСТИ (ФИЗИКИ) ---
		QScroller.grabGesture(
			self.viewport(),
			QScroller.ScrollerGestureType.LeftMouseButtonGesture
		)
		scroller = QScroller.scroller(self.viewport())
		props = QScrollerProperties()
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumVelocity, 0.15)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.DecelerationFactor, 0.25)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, 0.5)
		scroller.setScrollerProperties(props)
	
	def resizeEvent(self, event):
		super().resizeEvent(event)

		btn_w = MathScripts.coordinate_scaling(265)[0]
		btn_h = self.viewport().height()

		scroll_content = QWidget()
		scroll_content.setStyleSheet("background-color: transparent;")

		# Внутренние отступы самого скролла сбрасываем в 0, 
		# так как внешние 40 пикселей мы уже настроили в content_layout
		scroll_layout = QHBoxLayout(scroll_content)
		scroll_layout.setContentsMargins(0, 0, 0, 0)
		scroll_layout.setSpacing(15)

		for i in range(1, 8):
			sw = SwipeWidget(scroll_content)
			sw.set_button(width=btn_w, height=btn_h, radius=50, path_to_icon="./DataFile/Files.img/ThemeIcons/reload.svg")
			sw.set_label(text='pssss')
			scroll_layout.addWidget(sw)
			#btn = RoundedIconButton(width=btn_w, height=btn_h, radius=50, path_to_icon="./DataFile/Files.img/ThemeIcons/reload.svg")
			#btn.clicked.connect(lambda checked, num=i: print(f"Клик по кнопке {btn.width()} {btn.height()}!"))
			#scroll_layout.addWidget(btn)

		
		self.setWidget(scroll_content)
