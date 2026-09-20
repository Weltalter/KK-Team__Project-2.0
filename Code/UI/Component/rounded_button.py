from PyQt6.QtWidgets import QPushButton


class RoundedButton(QPushButton):
	def __init__(self, size: int = 20, parent=None):
		super().__init__(parent=parent)
		
		self._size = size
		
		self.setFixedSize(size, size)
		radius = size // 2
		
		self.setStyleSheet(f"""
			QPushButton {{
				border-radius: {radius}px;
			}}
		""")
