from PyQt6.QtWidgets import QLayout, QWidgetItem
from PyQt6.QtCore import QSize, QRect


class FlowItem:
	def __init__(self, item: QWidgetItem, x: int, y: int):
		self.item = item
		self.x = x
		self.y = y

class FlowLayout(QLayout):
	def __init__(self, parent=None):
		super().__init__(parent)
		self._items: list[FlowItem] = []

	def __del__(self):
		item = self.takeAt(0)
		while item:
			item = self.takeAt(0)

	def addWidget(self, widget, x: int = 0, y: int = 0):
		self.addChildWidget(widget)
		self.addItem(QWidgetItem(widget), x, y)

	def addItem(self, item: QWidgetItem, x: int = 0, y: int = 0):
		self._items.append(FlowItem(item, x, y))
		self.invalidate()

	def count(self) -> int:
		return len(self._items)

	def itemAt(self, index: int) -> QWidgetItem | None:
		if 0 <= index < len(self._items):
			return self._items[index].item
		return None

	def takeAt(self, index: int) -> QWidgetItem | None:
		if 0 <= index < len(self._items):
			coord_item = self._items.pop(index)
			return coord_item.item
		return None

	def setGeometry(self, rect: QRect):
		super().setGeometry(rect)
		
		for coord_item in self._items:
			item_size = coord_item.item.sizeHint()
			coord_item.item.setGeometry(
				QRect(
					rect.x() + coord_item.x, 
					rect.y() + coord_item.y, 
					item_size.width(), 
					item_size.height()
				)
			)

	def sizeHint(self) -> QSize:
		if not self._items:
			return QSize(100, 100)

		max_x = 0
		max_y = 0

		for coord_item in self._items:
			hint = coord_item.item.sizeHint()
			right_edge = coord_item.x + hint.width()
			bottom_edge = coord_item.y + hint.height()
			
			if right_edge > max_x:
				max_x = right_edge
			if bottom_edge > max_y:
				max_y = bottom_edge

		return QSize(max_x, max_y)

	def minimumSize(self) -> QSize:
		return self.sizeHint()

	def update_item_position(self, widget, new_x: int, new_y: int):
		for coord_item in self._items:
			if coord_item.item.widget() == widget:
				coord_item.x = new_x
				coord_item.y = new_y
				break
		self.invalidate()
