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
	
	def set_button(self, width: int = 20, height: int = 20, radius: int = 10, path_to_icon="./DataFile/Files.img/ThemeIcons/reload.svg"):
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
	__swipes_info: dict[int, str] = {
		0: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Фильмы"),
		1: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Игры"),
		2: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Рецепты"),
		3: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Книги"),
		4: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Лекарства"),
		5: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Сайты"),
		6: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Приложения"),
		7: ("./DataFile/Files.img/ThemeIcons/tmp.svg", "Счета"),
	}
	swipes_radius: int = 45
	swipes_width: int = 265

	def __init__(self, parent=None):
		super().__init__(parent=parent)
		self.__setting = Setting()
		self.setWidgetResizable(True)
		
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

		# --- НАСТРОЙКА ИНТЕНСИВНОСТИ (ФИЗИКИ) ---
		QScroller.grabGesture(
			self.viewport(),
			QScroller.ScrollerGestureType.MiddleMouseButtonGesture
		)
		scroller = QScroller.scroller(self.viewport())
		props = QScrollerProperties()
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MaximumVelocity, self.__setting.MaximumVelocity)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.DecelerationFactor, self.__setting.DecelerationFactor)
		props.setScrollMetric(QScrollerProperties.ScrollMetric.MousePressEventDelay, self.__setting.MousePressEventDelay)
		scroller.setScrollerProperties(props)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		
		card_w = btn_w = MathScripts.coordinate_scaling(self.swipes_width)[0]
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
				sw.set_button(width=btn_w, height=btn_h, radius=self.swipes_radius, path_to_icon=self.__swipes_info[i][0])
				sw.set_label(text=self.__swipes_info[i][1])
				self.__swipes_link[i] = sw
				scroll_layout.addWidget(self.__swipes_link[i])
		
		self.setWidget(scroll_content)
