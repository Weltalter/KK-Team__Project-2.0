import ctypes
import colorsys
from PyQt6.QtGui import QPixmap, QPainter, QColor


class MathScripts:
	@staticmethod
	def get_windows_scale_factor() -> float:
		"""Возвращает масштаб основного экрана Windows в виде float (например, 1.25 для 125%)."""
		try:
			percent = ctypes.windll.shcore.GetScaleFactorForDevice(0)
			return percent / 100.0
		except Exception:
			return 1.0

	@staticmethod
	def coordinate_scaling(*args: int) -> tuple[int, ...]:
		return tuple(int(x / MathScripts.get_windows_scale_factor()) for x in args)

	@staticmethod
	def adjust_brightness(hex_color: str, factor: float) -> str:
		"""
		Изменяет яркость HEX-цвета.
		:param hex_color: Строка вида '#3498db' или '3498db'
		:param factor: Коэффициент яркости (например, 0.9 для затемнения на 10%, 1.2 для осветления)
		"""
		hex_color = hex_color.lstrip('#')
		r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
		r, g, b = r / 255.0, g / 255.0, b / 255.0
		
		h, s, v = colorsys.rgb_to_hsv(r, g, b)
		
		v = max(0.0, min(v * factor, 1.0))
		
		r, g, b = colorsys.hsv_to_rgb(h, s, v)
		return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

	@staticmethod
	def pixmap_brightness(pixmap: QPixmap, factor: float) -> QPixmap:
		"""Программно затемняет картинку, рисуя поверх неё черный полупрозрачный слой."""
		result = QPixmap(pixmap)
		painter = QPainter(result)
		
		painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)
		
		alpha = int(255 * (1.0 - factor))
		
		painter.fillRect(result.rect(), QColor(0, 0, 0, alpha))
		painter.end()
		
		return result
