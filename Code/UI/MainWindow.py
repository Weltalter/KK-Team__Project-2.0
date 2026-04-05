from Code.Logic.AccessPoint import AP
from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.importData()
		self.setWindowSize()
		self.setCentralWidget(self.createUI())

	def importData(self):
		self.UI_coordinate = AP.getConst().Coordinate
		self.main_window_cor = self.UI_coordinate.get__main_window()

		self.UI_components = AP.getComponents()

	def setWindowSize(self):
		self.setMinimumSize(self.main_window_cor['window_minw'],
							self.main_window_cor['window_minh'])
		self.setMaximumSize(self.main_window_cor['window_maxw'],
							self.main_window_cor['window_maxh'])
		self.setGeometry(self.main_window_cor['window_x'],
						 self.main_window_cor['window_y'],
						 self.main_window_cor['window_w'],
						 self.main_window_cor['window_h'])

	def createUI(self) -> QWidget:
		window = QWidget()

		button = self.UI_components.IconButton(window)
		button.setGeometry(0, 0, 100, 100)
		button.setIcon(path_to_icon="trash.png")

		return window
