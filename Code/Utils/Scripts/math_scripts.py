import ctypes


class MathScripts:
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
