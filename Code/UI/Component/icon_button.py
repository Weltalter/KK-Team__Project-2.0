from PyQt6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtWidgets import QPushButton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.setting import Setting

class IconButton(QPushButton):
	def __init__(self, width: int = 80, height: int = 80, path_to_icon: str = None, parent=None):
		super().__init__(parent=parent)
		self.setFixedSize(width, height)
		self.setStyleSheet("background-color: transparent; border: none;")
		
		self.__setting = Setting()

		self._current_pixmap = None
		self._base_pixmap = None
		self._hover_pixmap = None
		self._pressed_pixmap = None

		if path_to_icon:
			self.setIcon(path_to_icon)

	def setIcon(self, path_to_icon: str):
		base = QPixmap(path_to_icon)
		if base.isNull():
			return
		
		self._base_pixmap = base.scaled(
			self.size(), 
			Qt.AspectRatioMode.IgnoreAspectRatio,
			Qt.TransformationMode.SmoothTransformation
		)
		
		self._hover_pixmap = MathScripts.pixmap_brightness(self._base_pixmap, self.__setting.hover_pixmap_brightness)
		self._pressed_pixmap = MathScripts.pixmap_brightness(self._base_pixmap, self.__setting.pressed_pixmap_brightness)
		
		self._current_pixmap = self._base_pixmap
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)

		rect = QRectF(1.0, 1.0, float(self.width() - 2), float(self.height() - 2))
		path = QPainterPath()
		path.addRect(rect)

		if self._current_pixmap:
			painter.save()
			painter.setClipPath(path)
			x = (self.width() - self._current_pixmap.width()) // 2
			y = (self.height() - self._current_pixmap.height()) // 2
			painter.drawPixmap(x, y, self._current_pixmap)
			painter.restore()
		
		painter.end()

	def enterEvent(self, event):
		super().enterEvent(event)
		if self._hover_pixmap:
			self._current_pixmap = self._hover_pixmap
			self.update()

	def leaveEvent(self, event):
		super().leaveEvent(event)
		if self._base_pixmap:
			self._current_pixmap = self._base_pixmap
			self.update()

	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			if self._pressed_pixmap:
				self._current_pixmap = self._pressed_pixmap
				self.update()
		super().mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		if self._hover_pixmap:
			self._current_pixmap = self._hover_pixmap
			self.update()
