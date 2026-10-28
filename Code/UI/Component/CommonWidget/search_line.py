from PyQt6.QtWidgets import (
	QWidget,
	QHBoxLayout,
)
from PyQt6.QtWidgets import QStyle, QStyleOption
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, pyqtSignal
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr
from Code.Utils.Constants.message import Message
from Code.Utils.Scripts.id_generator import IdGenerator
from Code.UI.Component.CommonWidget.rounded_text_button import RoundedTextButton
from Code.UI.Component.CommonWidget.flow_layout import FlowLayout
from Code.Utils.Constants.enum import FilterState


class SearchLine(QWidget):
	def __init__(self, width: int = None, height: int = None):
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()
		
		if width is not None:
			self.setFixedWidth(width)
		if height is not None:
			self.setFixedHeight(height)
		
		self.main_layout = QHBoxLayout(self)
		margin = 5
		self.main_layout.setContentsMargins(margin, margin, margin, margin)
		self.main_layout.setSpacing(self._coordinate.view_mode_btn_spacing)
	
	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
