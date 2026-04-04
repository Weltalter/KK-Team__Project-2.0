import sys
from PyQt6.QtWidgets import QApplication
from Code.Logic.Runtime import Runtime


if __name__ == "__main__":
	app = QApplication(sys.argv)
	_runtime = Runtime()
	_runtime.Run()
	app.exec()
