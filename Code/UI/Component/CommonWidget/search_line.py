from PyQt6.QtWidgets import (
	QWidget,
	QLineEdit,
	QHBoxLayout,
)
from PyQt6.QtWidgets import QStyle, QStyleOption
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, pyqtSignal
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.message import Message
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
		
		
		self.main_layout = FlowLayout(self)
		self.search_input = QLineEdit()
		self.test = RoundedTextButton(30, 30, 10, True, 12)

	def init_content(self):
		self.search_input.setObjectName("SearchImput")

		self.search_input.setFont(Fnt.shantell_sans(14))
		self.search_input.setPlaceholderText("Поиск...")
		self.search_input.setFixedHeight(40)

		self.test.set_text('1')
		self.test.set_color("#0bc141c0")

		self.main_layout.addWidget(self.search_input, 5, 5, fill_width=True, fill_height=True)
		self.main_layout.addWidget(self.test, 12, 12)
	
	def update_theme(self):
		self.setStyleSheet(f'''
			#SearchImput {{
				background-color: #2b2b2b;        /* Цвет фона (темно-серый) */
				border: 2px solid {Clr.sub_bg()};         /* Толщина, тип и цвет бордера (синий) */
				border-radius: 10px;                /* Скругление углов */
				color: {Clr.white()};                    /* Цвет самого текста при вводе */
				padding: 5px 75px 5px 8px;                  /* Внутренние отступы, чтобы текст не прилипал к краям */
			}}
		''')
		#self.setStyleSheet("background-color: red;")
	
	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)

	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
