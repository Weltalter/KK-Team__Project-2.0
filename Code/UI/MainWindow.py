from Code.Logic.AccessPoint import AP
from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setMinimumSize(AP.Get_Const().Coordinate.get__MainWindow()['window_minw'],
							AP.Get_Const().Coordinate.get__MainWindow()['window_minh'])
		self.setMaximumSize(AP.Get_Const().Coordinate.get__MainWindow()['window_maxw'],
							AP.Get_Const().Coordinate.get__MainWindow()['window_maxh'])
		self.setGeometry(AP.Get_Const().Coordinate.get__MainWindow()['window_x'],
						 AP.Get_Const().Coordinate.get__MainWindow()['window_y'],
						 AP.Get_Const().Coordinate.get__MainWindow()['window_w'],
						 AP.Get_Const().Coordinate.get__MainWindow()['window_h'])

		self.setCentralWidget(self.build_window())

	def build_window(self) -> QWidget:
		window = QWidget()
		return window
