import logging
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
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.rounded_icon_button import RoundedIconButton


class SwipeWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.__theme = Theme()
		self.setStyleSheet("background-color: transparent;")
		
		self.swipe_layout = QVBoxLayout(self)
		self.swipe_layout.setContentsMargins(0, 0, 0, 0)
		self.swipe_layout.setSpacing(15)

		self.btn = None
		self.lbl = None
	
	def set_button(self, width: int = 20, height: int = 20, radius: int = 10, path_to_icon=None):
		self.btn = RoundedIconButton(width=width, height=height, radius=radius, path_to_icon=path_to_icon)
		self.swipe_layout.addWidget(self.btn)

	def set_label(self, text: str = ''):
		self.lbl = QLabel(text)
		self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.lbl.setFont(self.__theme.get_main_font(font_size=24))
		
		self.lbl.setStyleSheet(f"QLabel {{ color: {self.__theme.font_color}; }}")

		self.swipe_layout.addWidget(self.lbl)

class MainMenuScrollArea(QScrollArea):
	__swipes_link: dict[int, SwipeWidget] = {}

	__swipes_radius: int = 45
	__swipes_width: int = 272

	def __init__(self, parent=None):
		super().__init__(parent=parent)
		logging.info('Инициализация виджета "MainMenuScrollArea"...')
		self.__setting = Setting()
		self.__message = Message()
		self.__icon = Icon()
		self.setWidgetResizable(True)
		
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

		self.__swipes_info: dict[int, str] = {
			0: (self.__icon.i_swipe_0, self.__message.swipe_0),
			1: (self.__icon.i_swipe_1, self.__message.swipe_1),
			2: (self.__icon.i_swipe_2, self.__message.swipe_2),
			3: (self.__icon.i_swipe_3, self.__message.swipe_3),
			4: (self.__icon.i_swipe_4, self.__message.swipe_4),
			5: (self.__icon.i_swipe_5, self.__message.swipe_5),
			6: (self.__icon.i_swipe_6, self.__message.swipe_6),
			7: (self.__icon.i_swipe_7, self.__message.swipe_7),
		}

		# --- НАСТРОЙКА ИНТЕНСИВНОСТИ (ФИЗИКИ) ---
		QScroller.grabGesture(
			self.viewport(),
			QScroller.ScrollerGestureType.MiddleMouseButtonGesture
		)
		scroller = QScroller.scroller(self.viewport())
		props = QScrollerProperties()
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumVelocity, self.__setting.maximum_velocity)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.DecelerationFactor, self.__setting.deceleration_factor)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, self.__setting.mouse_press_event_delay)
		scroller.setScrollerProperties(props)
		logging.info('Инициализация виджета "MainMenuScrollArea" завершена')

	def resizeEvent(self, event):
		super().resizeEvent(event)
		
		card_w = btn_w = MathScripts.coordinate_scaling(self.__swipes_width)[0]
		card_h = self.viewport().height()
		btn_h = card_h - 30
		
		scroll_content = QWidget()
		scroll_content.setStyleSheet("background-color: transparent;")
		
		scroll_layout = QHBoxLayout(scroll_content)
		scroll_layout.setContentsMargins(0, 0, 0, 0)
		scroll_layout.setSpacing(15)
		
		for i in range(len(self.__swipes_info)):
			if self.__swipes_link.get(i) is not None:
				self.__swipes_link[i].show()
			else:
				sw = SwipeWidget(scroll_content)
				sw.setFixedSize(card_w, card_h)
				sw.set_button(width=btn_w, height=btn_h, radius=self.__swipes_radius, path_to_icon=self.__swipes_info[i][0])
				sw.set_label(text=self.__swipes_info[i][1])
				self.__swipes_link[i] = sw
				scroll_layout.addWidget(self.__swipes_link[i])
		
		self.setWidget(scroll_content)
