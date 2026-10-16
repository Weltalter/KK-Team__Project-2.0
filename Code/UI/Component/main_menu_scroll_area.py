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
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.rounded_icon_button import RoundedIconButton


class SwipeWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self._coordinate = Coordinate()
		self.setStyleSheet("background-color: transparent;")
		
		self.swipe_layout = QVBoxLayout(self)
		self.swipe_layout.setContentsMargins(0, 0, 0, 0)
		self.swipe_layout.setSpacing(self._coordinate.main_menu_swipe_spacing)

		self.btn = None
		self.lbl = None
	
	def set_button(self, width: int = 20, height: int = 20, radius: int = 10, path_to_icon=None):
		self.btn = RoundedIconButton(width=width, height=height, radius=radius, path_to_icon=path_to_icon)
		self.swipe_layout.addWidget(self.btn)

	def set_label(self, text: str = ''):
		self.lbl = QLabel(text)
		self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.lbl.setFont(Fnt.shantell_sans(24))
		
		self.lbl.setStyleSheet(f"QLabel {{ color: {Clr.font()}; }}")

		self.swipe_layout.addWidget(self.lbl)

class MainMenuScrollArea(QScrollArea):
	_swipes_link: dict[int, SwipeWidget] = {}

	def __init__(self, width: int=800, parent=None):
		super().__init__(parent=parent)
		logging.info('Виджет "MainMenuScrollArea": Инициализация...')
		self._coordinate = Coordinate()
		self._setting = Setting()
		self._message = Message()
		self._icon = Icon()
		self.setFixedWidth(width)
		self.setWidgetResizable(True)
		
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

		self._swipes_info: dict[int, str] = {i: (self._icon.i_swipes[i], self._message.m_swipes[i]) for i in range(len(self._icon.i_swipes))}

		# --- НАСТРОЙКА ИНТЕНСИВНОСТИ (ФИЗИКИ) ---
		QScroller.grabGesture(
			self.viewport(),
			QScroller.ScrollerGestureType.MiddleMouseButtonGesture
		)
		scroller = QScroller.scroller(self.viewport())
		props = QScrollerProperties()
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumVelocity, self._setting.maximum_velocity)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.DecelerationFactor, self._setting.deceleration_factor)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, self._setting.mouse_press_event_delay)
		scroller.setScrollerProperties(props)
		logging.info('Виджет "MainMenuScrollArea": Инициализация завершена')

	def resizeEvent(self, event):
		super().resizeEvent(event)
		
		card_w = btn_w = MathScripts.coordinate_scaling(self._coordinate.main_menu_swipe_width)[0]
		card_h = self.viewport().height()
		btn_h = card_h - 30
		
		scroll_content = QWidget()
		scroll_content.setStyleSheet("background-color: transparent;")
		
		scroll_layout = QHBoxLayout(scroll_content)
		scroll_layout.setContentsMargins(0, 0, 0, 0)
		scroll_layout.setSpacing(self._coordinate.main_menu_scroll_spacing)
		
		for i in range(len(self._swipes_info)):
			if self._swipes_link.get(i) is not None:
				self._swipes_link[i].show()
			else:
				sw = SwipeWidget(scroll_content)
				sw.setFixedSize(card_w, card_h)
				sw.set_button(width=btn_w, height=btn_h, radius=self._coordinate.main_menu_swipe_radius, path_to_icon=self._swipes_info[i][0])
				sw.set_label(text=self._swipes_info[i][1])
				self._swipes_link[i] = sw
				scroll_layout.addWidget(self._swipes_link[i])
		
		self.setWidget(scroll_content)
