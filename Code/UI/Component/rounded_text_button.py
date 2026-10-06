from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QPushButton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.setting import Setting


class RoundedTextButton(QPushButton):
	def __init__(self, width: int = 20, height: int = 20, radius: int = 0, parent=None):
		super().__init__(parent=parent)
		self.setFixedSize(width, height)
		self.radius = radius

		self.__theme = Theme()
		self.__setting = Setting()

		self.setFont(self.__theme.get_shantell_sans(14))

		self.__current_color = None
		self.__base_color = None
		self.__hover_color = None
		self.__pressed_color = None

	def set_text(self, text: str = ''):
		self.setText(text)
		self.__update_style()

	def set_color(self, color: str = '#000000'):
		self.__current_color = color
		self.__base_color = color
		self.__hover_color = MathScripts.adjust_brightness(self.__base_color, self.__setting.hover_color_brightness)
		self.__pressed_color = MathScripts.adjust_brightness(self.__base_color, self.__setting.pressed_color_brightness)
		self.__update_style()

	def paintEvent(self, event):
		super().paintEvent(event)

		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		rect = QRectF(0, 0, float(self.width()), float(self.height()))
		path = QPainterPath()
		path.addRoundedRect(rect, self.radius, self.radius)

		pen = QPen(QColor(self.__theme.main_border_color), 2)
		painter.setPen(pen)
		painter.drawPath(path)

		painter.end()

	def __update_style(self):
		self.setStyleSheet(f"""
			QPushButton {{
				background-color: {self.__current_color};
				color: {self.__theme.font_color};
				border: none;
				border-radius: {self.radius}px;
				padding: 5px;
			}}
		""")

	def enterEvent(self, event):
		super().enterEvent(event)
		if self.__hover_color:
			self.__current_color = self.__hover_color
			self.__update_style()

	def leaveEvent(self, event):
		super().leaveEvent(event)
		if self.__base_color:
			self.__current_color = self.__base_color
			self.__update_style()

	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			if self.__pressed_color:
				self.__current_color = self.__pressed_color
				self.__update_style()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		if self.__hover_color:
			self.__current_color = self.__hover_color
			self.__update_style()
