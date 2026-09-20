import time
from PyQt6.QtGui import QRegion, QPixmap, QPainter, QPen
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt6.sip import isdeleted
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.UI.Component.rounded_button import RoundedButton


# ==========================================
# 1. Класс фонового воркера (таймера)
# ==========================================
class TimerWorker(QObject):
	spawn_button_signal = pyqtSignal(int)
	finished = pyqtSignal()

	def __init__(self, theme_count):
		super().__init__()
		self.is_running = True
		self.theme_count = theme_count

	def run(self):
		for i in range(1, self.theme_count):
			if self.is_running:
				self.spawn_button_signal.emit(i)
				time.sleep(0.1)
		
		self.finished.emit()

	def stop(self):
		self.is_running = False

class ThemeButton(RoundedButton):
	def __init__(self, size: int = 20, path_to_icon: str = None, parent=None):
		super().__init__(size=size, parent=parent)
		
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
		
		self._hover_pixmap = MathScripts.pixmap_brightness(self._base_pixmap, 0.85)
		self._pressed_pixmap = MathScripts.pixmap_brightness(self._base_pixmap, 0.70)
		
		self._current_pixmap = self._base_pixmap
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing) # Включаем идеальное сглаживание
		
		if self._current_pixmap:
			painter.save()
			
			clip_region = QRegion(1, 1, self.width() - 2, self.height() - 2, QRegion.RegionType.Ellipse)
			painter.setClipRegion(clip_region)
			
			x = (self.width() - self._current_pixmap.width()) // 2
			y = (self.height() - self._current_pixmap.height()) // 2
			painter.drawPixmap(x, y, self._current_pixmap)
			
			painter.restore()
		
		pen = QPen(Qt.GlobalColor.black, 2)
		painter.setPen(pen)
		
		painter.drawEllipse(1, 1, self.width() - 2, self.height() - 2)
		
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

class ThemeSubButton(ThemeButton):
	def __init__(self, theme_id: int = 0, size: int = 20, path_to_icon: str = None, theme_button=None, parent=None):
		super().__init__(size=size, path_to_icon=path_to_icon, parent=parent)
		self.id = theme_id
		self.theme_button = theme_button
		
		self.clicked.connect(self.__pick_theme)

	def __pick_theme(self):
		self.theme_button.change_theme(self.id)

class ThemeDropdown(ThemeButton):
	def __init__(self, size: int = 20, parent=None):
		super().__init__(size=size, parent=parent)
		
		self.__size = size
		self.__drop_thread = None
		self.__drop_worker = None
		self.__spawned_btn: dict[int, ThemeSubButton] = {}
		self.__icons: dict[int, str] = {
			0: "./DataFile/Files.img/ThemeIcons/canvas1.svg",
			1: "./DataFile/Files.img/ThemeIcons/canvas2.svg",
			2: "./DataFile/Files.img/ThemeIcons/canvas3.svg",
			3: "./DataFile/Files.img/ThemeIcons/canvas1.svg",
			4: "./DataFile/Files.img/ThemeIcons/canvas2.svg",
			5: "./DataFile/Files.img/ThemeIcons/canvas3.svg",
		}
		self.reload_mode_flag = False
		self.reload_mode_icon = "./DataFile/Files.img/ThemeIcons/reload.svg"
		self.current_theme_icon = "./DataFile/Files.img/ThemeIcons/canvas1.svg"
		
		self.setIcon(path_to_icon=self.current_theme_icon)
		self.clicked.connect(self.__dropdown)

	def __dropdown(self):
		if self.reload_mode_flag:
			if self.__drop_thread and not isdeleted(self.__drop_thread) and self.__drop_thread.isRunning():
				self.__drop_worker.stop()
			self.setIcon(path_to_icon=self.current_theme_icon)
			self.__hide_theme_subbutton()
			self.reload_mode_flag = False
			return
		
		self.__drop_thread = QThread()
		self.__drop_worker = TimerWorker(theme_count=len(self.__icons))
		self.__drop_worker.moveToThread(self.__drop_thread)
		
		self.__drop_thread.started.connect(self.__drop_worker.run)
		self.__drop_worker.spawn_button_signal.connect(self.__show_theme_subbutton)
		
		self.__drop_worker.finished.connect(self.__drop_thread.quit)
		self.__drop_worker.finished.connect(self.__drop_worker.deleteLater)
		self.__drop_thread.finished.connect(self.__drop_thread.deleteLater)
		
		self.__drop_thread.destroyed.connect(self.__clear_thread_references)
		
		self.reload_mode_flag = True
		self.setIcon(path_to_icon=self.reload_mode_icon)
		self.__drop_thread.start()

	def __show_theme_subbutton(self, index: int):
		current_geo = self.geometry()
		new_x = current_geo.x() - index * (current_geo.width() + 10)
		new_y = current_geo.y()
		
		new_btn = ThemeSubButton(theme_id=index,
						   		 size=self.__size,
						   		 path_to_icon=self.__icons[index],
								 theme_button=self,
								 parent=self.parentWidget())
		new_btn.setGeometry(new_x, new_y, self.__size, self.__size)
		new_btn.raise_()
		new_btn.show()
		
		self.__spawned_btn[index] = new_btn

	def __hide_theme_subbutton(self):
		for key in list(self.__spawned_btn.keys()):
			self.__spawned_btn[key].hide()
			self.__spawned_btn[key].deleteLater()
			del self.__spawned_btn[key]

	def change_theme(self, theme_id: int):
		self.current_theme_icon = self.__icons[theme_id]
		self.setIcon(path_to_icon=self.current_theme_icon)
		self.__hide_theme_subbutton()
		self.reload_mode_flag = False

	def __clear_thread_references(self):
		self.__drop_thread = None
		self.__drop_worker = None

	def destroy(self, destroyWindow=True, destroySubWindows=True):
		if self.__spawned_btn and not isdeleted(self.__spawned_btn):
			self.__spawned_btn.deleteLater()
		if self.__drop_worker:
			self.__drop_worker.stop()
		if self.__drop_thread:
			self.__drop_thread.quit()
			self.__drop_thread.wait()
		super().destroy(destroyWindow, destroySubWindows)
