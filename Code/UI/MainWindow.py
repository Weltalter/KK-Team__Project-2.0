from PyQt6.QtWidgets import (
	QMainWindow,
	QWidget,
)


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setMinimumSize(400, 300)
		self.setMaximumSize(1200, 800)
		self.setGeometry(710, 390, 500, 300)

		self.setCentralWidget(self.build_window())

	def build_window(self) -> QWidget:
		window = QWidget()
		return window
