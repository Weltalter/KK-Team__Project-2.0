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


class ElementViewModeButton(RoundedTextButton): # TODO: Поменять RoundedTextButton на RoundedIconButton
	def __init__(self, mode, width: int = 20, height: int = 20, radius: int = 20, parent=None):
		super().__init__(width=width, height=height, radius=radius, parent=parent)
		self._mode: ElementViewMode = mode
		self._parent: ElementViewModeManager = parent
		
		self.clicked.connect(self._change_mode)

	def _change_mode(self):
		self._parent.mode_changed.emit(self._mode)

class ElementViewModeManager(QWidget):
	mode_changed = pyqtSignal(ElementViewMode)
	_modes: dict[ElementViewMode, ElementViewModeButton] = {}

	def __init__(self):
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()
		
		self.main_layout = QHBoxLayout(self)
		self.main_layout.setContentsMargins(5, 5, 5, 5) # TODO: Поменять на файловые константы
		self.main_layout.setSpacing(5)

	def register_modes(self, modes: list[ElementViewMode]):
		for mode in modes:
			new_btn = ElementViewModeButton(mode=mode,
			                                width=50, # TODO: Поменять на файловые константы
											height=50,
											radius=10,
											parent=self)
			new_btn.set_text(str(mode.value)) # TODO: Поменять на иконки
			new_btn.raise_()
			self._modes[mode] = new_btn
			self.main_layout.addWidget(new_btn)

	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
	
	def update_theme(self):
		for btn in list(self._modes.values()):
			btn.set_color(Clr.sub_bg())
	
	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()