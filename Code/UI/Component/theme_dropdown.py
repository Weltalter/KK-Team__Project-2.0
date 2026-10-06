import time
import logging
from PyQt6.QtCore import QThread, QObject, pyqtSignal
from PyQt6.sip import isdeleted
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.rounded_icon_button import RoundedIconButton


# ==========================================
#     Класс фонового воркера (таймера)
# ==========================================
class TimerWorker(QObject):
	spawn_button_signal = pyqtSignal(int)
	finished = pyqtSignal()

	def __init__(self, theme_count):
		super().__init__()
		self.is_running = True
		self.__theme_count = theme_count

	def run(self):
		for i in range(0, self.__theme_count):
			if self.is_running:
				self.spawn_button_signal.emit(i)
				time.sleep(0.1)
		
		self.finished.emit()

	def stop(self):
		self.is_running = False

class ThemeSubButton(RoundedIconButton):
	def __init__(self, theme_id: int = 0, size: int = 20, path_to_icon: str = None, theme_button=None, parent=None):
		super().__init__(width=size, height=size, radius=size//2, path_to_icon=path_to_icon, parent=parent)
		self.id = theme_id
		self.__theme_button = theme_button
		
		self.clicked.connect(self.__pick_theme)

	def __pick_theme(self):
		self.__theme_button.change_theme(self.id)

class ThemeDropdown(RoundedIconButton):
	def __init__(self, size: int = 20, parent=None):
		super().__init__(width=size, height=size, radius=size//2, parent=parent)
		logging.info('Виджет "ThemeDropdown": Инициализация...')
		self.__coordinate = Coordinate()
		self.__setting = Setting()
		self.__icon = Icon()

		self.__parent = parent
		
		self.__size = size
		self.__drop_thread = None
		self.__drop_worker = None
		self.__spawned_btn: dict[int, ThemeSubButton] = {}
		self.__icons: dict[int, str] = {i: self.__icon.i_themes[i] for i in range(len(self.__icon.i_themes))}
		self.reload_mode_flag = False
		self.reload_mode_icon = self.__icon.i_reload
		self.current_theme_icon = self.__icons[self.__setting.theme_id]
		
		self.setIcon(path_to_icon=self.current_theme_icon)
		self.clicked.connect(self.__dropdown)
		logging.info('Виджет "ThemeDropdown": Инициализация завершена')

	def __dropdown(self):
		logging.info('Раскрытие списка тем "ThemeDropdown"')
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
		new_x = current_geo.x() - (index + 1) * (current_geo.width() + self.__coordinate.header_theme_btn_offset)
		new_y = current_geo.y()
		
		new_btn = ThemeSubButton(theme_id=index,
						   		 size=self.__size,
						   		 path_to_icon=self.__icons[index],
								 theme_button=self,
								 parent=self.__parent)
		new_btn.setGeometry(new_x, new_y, self.__size, self.__size)
		new_btn.raise_()
		new_btn.show()
		
		self.__spawned_btn[index] = new_btn

	def __hide_theme_subbutton(self):
		for key in list(self.__spawned_btn.keys()):
			self.__spawned_btn[key].hide()
			self.__spawned_btn[key].deleteLater()
			del self.__spawned_btn[key]
		logging.info('Закрытие списка тем "ThemeDropdown"')

	def change_theme(self, theme_id: int):
		if self.__drop_thread and not isdeleted(self.__drop_thread) and self.__drop_thread.isRunning():
			self.__drop_worker.stop()

		self.__setting.theme_id = theme_id
		self.current_theme_icon = self.__icons[theme_id]
		self.setIcon(path_to_icon=self.current_theme_icon)
		self.reload_mode_flag = False
		logging.info(f'Выбрана тема {theme_id}')
		self.__hide_theme_subbutton()

	def __clear_thread_references(self):
		self.__drop_thread = None
		self.__drop_worker = None

	def destroy(self, destroyWindow=True, destroySubWindows=True):
		self.__stop_spawn_process()
		for btn in list(self.__spawned_btn.values()):
			if not isdeleted(btn):
				btn.deleteLater()
		self.__spawned_btn.clear()
		super().destroy(destroyWindow, destroySubWindows)
