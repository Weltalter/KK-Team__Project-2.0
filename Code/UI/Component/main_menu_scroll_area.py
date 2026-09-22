import os
from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
	QScrollArea,
	QScroller,
	QScrollerProperties,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QFont
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.UI.Component.rounded_icon_button import RoundedIconButton


class SwipeWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.setStyleSheet("background-color: transparent;")
		
		self.swipe_layout = QVBoxLayout(self)
		self.swipe_layout.setContentsMargins(0, 0, 0, 0)
		self.swipe_layout.setSpacing(15)

		self.btn = None
		self.lbl = None
	
	def set_button(self, width: int = 20, height: int = 20, radius: int = 10, path_to_icon="./DataFile/Files.img/ThemeIcons/reload.svg"):
		self.btn = RoundedIconButton(width=width, height=height, radius=radius, path_to_icon=path_to_icon)
		self.swipe_layout.addWidget(self.btn)

	def set_label(self, text: str = ''):
		self.lbl = QLabel(text)
		self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
		font_size = MathScripts.coordinate_scaling(24)[0]
		font_path = os.path.abspath("./DataFile/Files.font/Shantell Sans/ShantellSans-Medium.ttf")
		
		font_id = QFontDatabase.addApplicationFont(font_path)
		font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
		
		font = QFont(font_family, font_size)
		font.setWeight(QFont.Weight.Medium)
		self.lbl.setFont(font)
		
		self.lbl.setStyleSheet("QLabel { color: #ffffff; }")

		self.swipe_layout.addWidget(self.lbl)

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
		
		self.__swipes: dict[int, str] = {
			0: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Фильмы"),
			1: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Игры"),
			2: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Рецепты"),
			3: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Книги"),
			4: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Лекарства"),
			5: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Сайты"),
			6: ("./DataFile/Files.img/ThemeIcons/reload.svg", "Приложения"),
		}

	def resizeEvent(self, event):
		super().resizeEvent(event)
		
		card_w = btn_w = MathScripts.coordinate_scaling(265)[0]
		card_h = self.viewport().height()
		btn_h = card_h - 30
		
		scroll_content = QWidget()
		scroll_content.setStyleSheet("background-color: transparent;")
		
		# Внутренние отступы самого скролла сбрасываем в 0, 
		# так как внешние 40 пикселей мы уже настроили в content_layout
		scroll_layout = QHBoxLayout(scroll_content)
		scroll_layout.setContentsMargins(0, 0, 0, 0)
		scroll_layout.setSpacing(15)
		
		for i in range(7):
			sw = SwipeWidget(scroll_content)
			sw.setFixedSize(card_w, card_h)
			sw.set_button(width=btn_w, height=btn_h, radius=45, path_to_icon=self.__swipes[i][0])
			sw.set_label(text=self.__swipes[i][1])
			scroll_layout.addWidget(sw)
		
		self.setWidget(scroll_content)
