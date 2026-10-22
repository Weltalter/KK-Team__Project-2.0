from PyQt6.QtWidgets import QLayout, QLayoutItem
from PyQt6.QtCore import Qt, QPoint, QRect, QSize


class FlowLayout(QLayout):
	def __init__(self, parent=None, margin=-1, spacing=-1):
		super().__init__(parent)
		if margin >= 0:
			self.setContentsMargins(margin, margin, margin, margin)
		self.setSpacing(spacing if spacing >= 0 else 6)
		self._items = []

	def __del__(self):
		del self._items

	def addItem(self, item: QLayoutItem):
		self._items.append(item)

	def count(self) -> int:
		return len(self._items)

	def itemAt(self, index: int) -> QLayoutItem:
		if 0 <= index < len(self._items):
			return self._items[index]
		return None

	def takeAt(self, index: int) -> QLayoutItem:
		if 0 <= index < len(self._items):
			return self._items.pop(index)
		return None

	def expandingDirections(self) -> Qt.Orientation:
		return Qt.Orientation(0)

	def hasHeightForWidth(self) -> bool:
		return True

	def heightForWidth(self, width: int) -> int:
		return self._do_layout(QRect(0, 0, width, 0), test_only=True)

	def setGeometry(self, rect: QRect):
		super().setGeometry(rect)
		self._do_layout(rect, test_only=False)

	def sizeHint(self) -> QSize:
		return self._minimum_size()

	def minimumSize(self) -> QSize:
		return self._minimum_size()

	def _do_layout(self, rect: QRect, test_only: bool) -> int:
		left, top, right, bottom = self.getContentsMargins()
		effective_rect = rect.adjusted(+left, +top, -right, -bottom)
		x = effective_rect.x()
		y = effective_rect.y()
		line_height = 0
		spacing = self.spacing()

		for item in self._items:
			widget = item.widget()
			space_x = spacing
			space_y = spacing
			
			# Рассчитываем идеальный размер для элемента
			size = item.sizeHint()
			next_x = x + size.width() + space_x
			
			# Если элемент выходит за границы по ширине, переносим на новую строку
			if next_x - space_x > effective_rect.right() and line_height > 0:
				x = effective_rect.x()
				y = y + line_height + space_y
				next_x = x + size.width() + space_x
				line_height = 0

			if not test_only:
				item.setGeometry(QRect(QPoint(x, y), size))

			x = next_x
			line_height = max(line_height, size.height())

		return y + line_height - rect.y() + bottom

	def _minimum_size(self) -> QSize:
		size = QSize()
		for item in self._items:
			size = size.expandedTo(item.minimumSize())
		left, top, right, bottom = self.getContentsMargins()
		size += QSize(left + right, top + bottom)
		return size