from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QPushButton
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Theme
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.icon import Icon


class RoundedIconButton(QPushButton):
	def __init__(self, width: int = 20, height: int = 20, radius: int = 0, path_to_icon: str = None, parent=None):
		super().__init__(parent=parent)
		self.setFixedSize(width, height)

		self.__theme = Theme()
		self.__setting = Setting()
		self.__icon = Icon()

		self.radius = radius
		self._current_pixmap = None
		self._base_pixmap = None
		self._hover_pixmap = None
		self._pressed_pixmap = None

		if path_to_icon:
			self.setIcon(path_to_icon)

	def setIcon(self, path_to_icon: str):
		if path_to_icon is None:
			path_to_icon = self.__icon.i_reload
		if path_to_icon.lower().endswith('.svg'):
			screen = self.screen() if self.window() else None
			dpr = screen.devicePixelRatio() if screen else 1.0
			
			target_width = int(self.width() * dpr)
			target_height = int(self.height() * dpr)
			
			base = QPixmap(target_width, target_height)
			base.fill(Qt.GlobalColor.transparent)
			
			renderer = QSvgRenderer(path_to_icon)
			painter = QPainter(base)
			painter.setRenderHint(QPainter.RenderHint.Antialiasing)
			painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
			
			padding = 4.0 * dpr
			
			render_rect = QRectF(
				padding, 
				padding, 
				float(target_width) - (padding * 2.0), 
				float(target_height) - (padding * 2.0)
			)
			
			renderer.render(painter, render_rect)
			painter.end()
			
			base.setDevicePixelRatio(dpr)
		else:
			base = QPixmap(path_to_icon)
			if base.isNull():
				return
		
			base = base.scaled(
				self.size(), 
				Qt.AspectRatioMode.IgnoreAspectRatio,
				Qt.TransformationMode.SmoothTransformation
			)

		self._base_pixmap = base
		self._hover_pixmap = MathScripts.pixmap_brightness(self._base_pixmap, self.__setting.hover_pixmap_brightness)
		self._pressed_pixmap = MathScripts.pixmap_brightness(self._base_pixmap, self.__setting.pressed_pixmap_brightness)
		
		self._current_pixmap = self._base_pixmap
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

		rect = QRectF(1.0, 1.0, float(self.width() - 2), float(self.height() - 2))
		path = QPainterPath()
		path.addRoundedRect(rect, self.radius, self.radius)

		if self._current_pixmap:
			painter.save()
			painter.setClipPath(path)
			
			p_width = float(self._current_pixmap.width())
			p_height = float(self._current_pixmap.height())
			
			x = (float(self.width()) - p_width) / 2.0
			y = (float(self.height()) - p_height) / 2.0
			
			target_rect = QRectF(x, y, p_width, p_height)
			
			painter.drawPixmap(target_rect, self._current_pixmap, QRectF(self._current_pixmap.rect()))
			painter.restore()

		pen = QPen(QColor(self.__theme.main_border_color), 2)
		painter.setPen(pen)
		
		painter.drawPath(path)

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
