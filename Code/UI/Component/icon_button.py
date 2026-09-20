from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon

class IconButton(QPushButton):
	def __init__(self, path_to_icon: str = None, parent=None):
		super().__init__(parent=parent)
		self.setStyleSheet("background-color: transparent; border: none;")
		self.clicked.connect(lambda: print("click"))
		
		if path_to_icon:
			self.setIcon(path_to_icon)

	def setIcon(self, path_to_icon: str):
		icon = QIcon(path_to_icon)
		super().setIcon(icon)
		self.setIconSize(self.size())

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.setIconSize(self.size())
