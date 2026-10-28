from PyQt6.QtWidgets import (
	QWidget,
	QHBoxLayout,
	QVBoxLayout,
)
from PyQt6.QtWidgets import QStyle, QStyleOption
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr
from Code.Utils.Constants.message import Message
from Code.UI.Component.element_view_mode_manager import ElementViewModeManager
from Code.UI.Component.hashtag_filter_manager import HashtagFilterManager
from Code.Utils.Constants.enum import ElementViewMode


class MovieMenu(QWidget):
	_element_view_mode: ElementViewMode = ElementViewMode.LIST

	def __init__(self, manager):
		self.manager = manager
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()
		
		self.setObjectName("MovieMenu")

		main_layout = QVBoxLayout(self)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		#region Область поиска
		search_area_widget = QWidget()
		search_area_widget.setObjectName("SearchArea")
		search_area_widget.setStyleSheet("background-color: transparent;")
		
		search_area_layout = QVBoxLayout(search_area_widget)
		search_area_layout.setContentsMargins(0, 0, 0, 0)
		search_area_layout.setSpacing(0)

		#region Область поисковой строки
		searching_line_widget = QWidget()
		searching_line_widget.setObjectName("SearchingLine")
		searching_line_widget.setStyleSheet("background-color: #a0a0a0;")

		searching_line_widget.setFixedSize(600, 40)
		#endregion
		
		#region Область фильтра
		filter_area_widget = QWidget()
		filter_area_widget.setObjectName("FilterArea")
		filter_area_widget.setStyleSheet("background-color: transparent;")
		
		filter_area_layout = QHBoxLayout(filter_area_widget)
		filter_area_layout.setContentsMargins(0, 0, 0, 0)
		filter_area_layout.setSpacing(0)

		#region Область хэштегов
		hashtag_choice_widget = HashtagFilterManager()
		hashtag_choice_widget.setObjectName("HashtagFilter")
		hashtag_choice_widget.setStyleSheet("background-color: transparent;")
		#endregion

		#region Область размера иконок
		element_view_mode_widget = ElementViewModeManager()
		element_view_mode_widget.setObjectName("ElementViewMode")
		element_view_mode_widget.setStyleSheet("background-color: transparent;")

		element_view_mode_widget.register_modes(modes=[ElementViewMode.LIST, ElementViewMode.POSTER, ElementViewMode.INFO])
		element_view_mode_widget.mode_changed.connect(self._element_view_mode_changed)
		#endregion

		filter_area_layout.addWidget(hashtag_choice_widget, stretch=1)
		filter_area_layout.addWidget(element_view_mode_widget, stretch=0, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
		#endregion

		search_area_layout.addWidget(searching_line_widget, stretch=0, alignment=Qt.AlignmentFlag.AlignHCenter)
		search_area_layout.addWidget(filter_area_widget, stretch=1)
		#endregion

		#region Область контента
		content_area_widget = QWidget()
		content_area_widget.setObjectName("ContentArea")
		
		content_area_layout = QVBoxLayout(content_area_widget)
		content_area_layout.setContentsMargins(0, 0, 0, 0)
		content_area_layout.setSpacing(0)
		#endregion

		main_layout.addWidget(search_area_widget, stretch=0)
		main_layout.addWidget(content_area_widget, stretch=1)

	def _element_view_mode_changed(self, new_mode: ElementViewMode):
		if self._element_view_mode != new_mode:
			self._element_view_mode = new_mode
	
	def update_theme(self):
		self.setStyleSheet(f'''
			#MovieMenu {{
				background-color: {Clr.main_bg()};
			}}
		''')

	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
	
	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
		Clr.subscribe(self.update_theme)
	