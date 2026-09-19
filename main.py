import sys
from PyQt6.QtWidgets import QApplication
from Code.Logic.runtime import Runtime


if __name__ == "__main__":
	app = QApplication(sys.argv)
	runtime = Runtime()
	runtime.run()
	app.exec()
