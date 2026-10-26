from PyQt6.QtWidgets import (
	QWidget,
	QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Scripts.id_generator import IdGenerator
from Code.UI.Component.CommonWidget.rounded_text_button import RoundedTextButton
from Code.UI.Component.CommonWidget.flow_layout import FlowLayout
from Code.Utils.Constants.enum import FilterState


class FilterButton(RoundedTextButton):
	_index: int = None
	_filter_state: FilterState = FilterState.NEUTRAL
	filter_changed = pyqtSignal(int, FilterState)

	def __init__(self, index: int, text: str):
		self._coordinate = Coordinate()

		width, height = Fnt.px_size(Fnt.shantell_sans(14), text)
		btn_padding = self._coordinate.button_padding * 2

		super().__init__(width=width+btn_padding, height=height+btn_padding, radius=-1, font_size=10)

		self._index = index
		self.set_text(text)
		self.set_color(Clr.filter_bg(self._filter_state))
		self.clicked.connect(self._change_state)

	def change_index(self, new_index: int):
		self._index = new_index

	def _change_state(self):
		self.filter_changed.emit(self._index, self._filter_state)
		self._filter_state = FilterState((self._filter_state + 1) % 3)
		self.set_color(Clr.filter_bg(self._filter_state))

class FilterField(QScrollArea):
	def __init__(self, height=100):
		super().__init__()
		self._coordinate = Coordinate()

		self._filter = {FilterState.NEUTRAL: {}, FilterState.DISABLE: {}, FilterState.ENABLE: {}}
		self._all_btn = []
		self._generator = {FilterState.NEUTRAL: IdGenerator(), FilterState.DISABLE: IdGenerator(), FilterState.ENABLE: IdGenerator()}
		
		self.setFixedHeight(height)
		self.setWidgetResizable(True)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		self.setStyleSheet("QScrollArea { border: none; background-color: #0fa1a1; }")

		self.container = QWidget()
		self.container.setStyleSheet("background-color: transparent;") 
		
		self.layout = FlowLayout(self.container)
		
		self.setWidget(self.container)

	def init_filter(self, filters: list[str]):
		for text in filters:
			btn_id = self._generator[FilterState.NEUTRAL].get_id()
			btn = FilterButton(index=btn_id, text=text)
			btn.filter_changed.connect(self.filter_changed)

			self._filter[FilterState.NEUTRAL][btn_id] = btn
			self._all_btn.append(btn)
			
			self.layout.addWidget(btn, 0, 0)
		QTimer.singleShot(0, self._reposition_buttons)


	def _reposition_buttons(self):
		padding = 10
		x_cor = padding
		y_cor = padding
		max_width = self.viewport().width()

		for btn in self._all_btn:
			btn.move(x_cor, y_cor)

			x_cor += btn.width() + padding
			if x_cor + btn.width() + padding > max_width:
				x_cor = padding
				y_cor += btn.height() + padding

	def filter_changed(self, index: int, state: FilterState):
		btn_state = FilterState((state + 1) % 3)
		btn_id = self._generator[btn_state].get_id()

		self._filter[btn_state][btn_id] = self._filter[state][index]
		self._filter[btn_state][btn_id].change_index(btn_id)

		del self._filter[state][index]
		self._generator[state].release_id(index)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self._reposition_buttons()