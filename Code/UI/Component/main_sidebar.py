from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QStyle, QStyleOption
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty 

class MainSidebar(QWidget):
	def __init__(self, collaps_width, expand_width, parent=None):
		super().__init__(parent=parent)

		self._collapsed_width = collaps_width
		self._expanded_width = expand_width
		
		self.setFixedWidth(self._collapsed_width)

		self.animation = QPropertyAnimation(self, b"sidebar_width")
		self.animation.setDuration(200)
		self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

	@pyqtProperty(int)
	def sidebar_width(self) -> int:
		return self.width()

	@sidebar_width.setter
	def sidebar_width(self, width: int):
		self.setFixedWidth(width)

	def enterEvent(self, event):
		super().enterEvent(event)
		self.animation.stop()
		self.animation.setStartValue(self.width())
		self.animation.setEndValue(self._expanded_width)
		self.animation.start()

	def leaveEvent(self, event):
		super().leaveEvent(event)
		self.animation.stop()
		self.animation.setStartValue(self.width())
		self.animation.setEndValue(self._collapsed_width)
		self.animation.start()

	def paintEvent(self, event):
		opt = QStyleOption()
		opt.initFrom(self)
		painter = QPainter(self)
		self.style().drawPrimitive(QStyle.PrimitiveElement.PE_Widget, opt, painter, self)
