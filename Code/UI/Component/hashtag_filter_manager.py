from PyQt6.QtWidgets import (
	QWidget,
	QHBoxLayout,
	QVBoxLayout,
	QLabel,
)
from PyQt6.QtWidgets import QStyle, QStyleOption
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.enum import ElementViewMode
from Code.UI.Component.CommonWidget.filter_field import FilterField


class HashtagFilterManager(QWidget):
	hashtag_changed = pyqtSignal(tuple)

	def __init__(self):
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()
		
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5) # TODO: Поменять на файловые константы

		self.filter_field = FilterField(height=100)
		self.filter_field.init_filter(['дом', 'мост', 'ветер', 'гитара', 'облако',
		                               'радуга', 'солнце', 'яблоко', 'аквариум',
									   'бабочка', 'деревня', 'микрофон', 'самовар',
									   'картофель', 'компьютер', 'велосипед',
									   'космонавт', 'фотография', 'библиотека',
									   'электричество'])
		self.main_layout.addWidget(self.filter_field, stretch=1)

