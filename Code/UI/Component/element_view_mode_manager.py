from PyQt6.QtWidgets import (
	QWidget,
	QHBoxLayout,
)
from PyQt6.QtWidgets import QStyle, QStyleOption
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QPainter
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.enum import ElementViewMode
from Code.UI.Component.CommonWidget.rounded_text_button import RoundedTextButton


class ElementViewModeButton(RoundedTextButton): # TODO: Поменять RoundedTextButton на RoundedIconButton
	def __init__(self, mode, width: int = 20, height: int = 20, radius: int = 20, parent=None):
		super().__init__(width=width, height=height, radius=radius, border_flag=True, parent=parent)
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
		margin = self._coordinate.view_mode_manager_margin
		self.main_layout.setContentsMargins(margin, margin, margin, margin)
		self.main_layout.setSpacing(self._coordinate.view_mode_btn_spacing)

	def register_modes(self, modes: list[ElementViewMode]):
		for mode in modes:
			new_btn = ElementViewModeButton(mode=mode,
											width=self._coordinate.view_mode_btn_width,
											height=self._coordinate.view_mode_btn_height,
											radius=self._coordinate.view_mode_btn_radius,
											parent=self)
			new_btn.set_text(str(mode.value)) # TODO: Поменять на иконки
			new_btn.raise_()
			self._modes[mode] = new_btn
			self.main_layout.addWidget(new_btn)

	def update_theme(self):
		for btn in list(self._modes.values()):
			btn.set_color(Clr.sub_bg())
	
	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
	
	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
