from Code.Logic.AccessPoint import AP
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon

class IconButton(QPushButton):
	def __init__(self, parent):
		super().__init__(parent=parent)
		self.setStyleSheet("background-color: transparent;")
		self.clicked.connect(lambda: print("click"))

	def setIcon(self, path_to_icon: str):
		icon = QIcon(path_to_icon)
		super().setIcon(icon)
