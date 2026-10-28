from PyQt6.QtWidgets import (
	QWidget,
	QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.message import Message
from Code.UI.Component.CommonWidget.filter_field import FilterField


class HashtagFilterManager(QWidget):
	hashtag_changed = pyqtSignal(tuple)

	def __init__(self):
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()
		
		self.main_layout = QHBoxLayout(self)
		margin = self._coordinate.hashtag_filter_manager_margin
		self.main_layout.setContentsMargins(margin, margin, margin, margin)

		self.filter_field = FilterField(height=self._coordinate.hashtag_filter_manager_height)
		self.filter_field.init_filter(['дом', 'мост', 'ветер', 'гитара', 'облако',
									   'радуга', 'солнце', 'яблоко', 'аквариум',
									   'бабочка', 'деревня', 'микрофон', 'самовар',
									   'картофель', 'компьютер', 'велосипед',
									   'космонавт', 'фотография', 'библиотека',
									   'электричество', 'дом', 'мост', 'ветер', 'гитара', 'облако',
									   'радуга', 'солнце', 'яблоко', 'аквариум',
									   'бабочка', 'деревня', 'микрофон', 'самовар',
									   'картофель', 'компьютер', 'велосипед',
									   'космонавт', 'фотография', 'библиотека',
									   'электричество', 'дом', 'мост', 'ветер', 'гитара', 'облако',
									   'радуга', 'солнце', 'яблоко', 'аквариум',
									   'бабочка', 'деревня', 'микрофон', 'самовар',
									   'картофель', 'компьютер', 'велосипед',
									   'космонавт', 'фотография', 'библиотека',
									   'электричество'])
		self.main_layout.addWidget(self.filter_field, stretch=1)

