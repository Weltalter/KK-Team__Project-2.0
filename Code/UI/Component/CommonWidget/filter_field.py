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
from Code.UI.Component.CommonWidget.rounded_text_button import RoundedTextButton
from Code.Utils.Constants.enum import ElementViewMode, FilterState


class FilterField(QWidget):
	_filter: dict[FilterState, list[str]] = {FilterState.DISABLE: [], FilterState.ENABLE: []}

	def __init__(self):
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()

	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
