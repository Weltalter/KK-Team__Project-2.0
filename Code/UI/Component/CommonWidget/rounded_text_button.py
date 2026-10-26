from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QPushButton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting


class RoundedTextButton(QPushButton):
	def __init__(self, width: int = 20, height: int = 20, radius: int = 0, font_size: int = 14, parent=None):
		super().__init__(parent=parent)
		self.setFixedSize(width, height)
		self.radius = radius

		self._setting = Setting()
		self._coordinate = Coordinate()

		self.setFont(Fnt.shantell_sans(font_size))

		self._current_color = None
		self._base_color = None
		self._hover_color = None
		self._pressed_color = None

	def set_text(self, text: str = ''):
		self.setText(text)
		self._update_style()

	def set_color(self, color: str = '#000000'):
		self._current_color = color
		self._base_color = color
		self._hover_color = MathScripts.adjust_brightness(self._base_color, self._setting.hover_color_brightness)
		self._pressed_color = MathScripts.adjust_brightness(self._base_color, self._setting.pressed_color_brightness)
		self._update_style()

	def paintEvent(self, event):
		super().paintEvent(event)

		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		rect = QRectF(0, 0, float(self.width()), float(self.height()))
		path = QPainterPath()
		path.addRoundedRect(rect, self.radius, self.radius)

		pen = QPen(QColor(Clr.main_brd()), 2)
		painter.setPen(pen)
		painter.drawPath(path)

		painter.end()

	def _update_style(self):
		self.setStyleSheet(f"""
			QPushButton {{
				background-color: {self._current_color};
				color: {Clr.font()};
				border: none;
				border-radius: {self.radius}px;
				padding: {self._coordinate.button_padding}px;
			}}
		""")

	def enterEvent(self, event):
		super().enterEvent(event)
		if self._hover_color:
			self._current_color = self._hover_color
			self._update_style()

	def leaveEvent(self, event):
		super().leaveEvent(event)
		if self._base_color:
			self._current_color = self._base_color
			self._update_style()

	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			if self._pressed_color:
				self._current_color = self._pressed_color
				self._update_style()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		if self._hover_color:
			self._current_color = self._hover_color
			self._update_style()
