from PyQt6.QtWidgets import (
	QWidget,
	QHBoxLayout,
	QLabel,
)
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.message import Message


class MedicineMenu(QWidget):
	def __init__(self, manager):
		self.manager = manager
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()

		main_layout = QHBoxLayout(self)
		main_layout.setContentsMargins(0, 0, 0, 0)
		main_layout.setSpacing(0)

		test = QLabel("Medicine")
		test.setFont(Fnt.shantell_sans(14))

		main_layout.addWidget(test)
		
	def update_theme(self):
		pass

	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
		Clr.subscribe(self.update_theme)
	