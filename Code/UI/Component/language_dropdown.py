import time
import logging
from PyQt6.QtCore import QThread, QObject, pyqtSignal
from PyQt6.sip import isdeleted
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.theme import Theme
from Code.UI.Component.button import Button


# ==========================================
#     Класс фонового воркера (таймера)
# ==========================================
class TimerWorker(QObject):
	spawn_button_signal = pyqtSignal(int)
	finished = pyqtSignal()

	def __init__(self, language_count):
		super().__init__()
		self.is_running = True
		self.__language_count = language_count

	def run(self):
		for i in range(0, self.__language_count):
			if self.is_running:
				self.spawn_button_signal.emit(i)
				time.sleep(0.1)
		
		self.finished.emit()

	def stop(self):
		self.is_running = False

class LanguageSubButton(Button):
	def __init__(self, language_id: int = 0, width: int = 20, height: int = 20, radius: int = 20, language_button=None, parent=None):
		super().__init__(width=width, height=height, radius=radius, parent=parent)
		self.id = language_id
		self.__language_button = language_button
		
		self.clicked.connect(self.__pick_language)

	def __pick_language(self):
		self.__language_button.change_language(self.id)

class LanguageDropdown(Button):
	def __init__(self, width: int = 20, height: int = 20, radius: int = 20, parent=None):
		super().__init__(width=width, height=height, radius=radius, parent=parent)
		logging.info('Виджет "LanguageDropdown": Инициализация...')
		self.__coordinate = Coordinate()
		self.__setting = Setting()
		self.__message = Message()
		self.__theme = Theme()
		
		self.__width = width
		self.__height = height
		self.__drop_thread = None
		self.__drop_worker = None
		self.__spawned_btn: dict[int, LanguageSubButton] = {}
		self.__texts: dict[int, str] = {i: self.__message.m_languages[i] for i in range(len(self.__message.m_languages))}
		self.reload_mode_flag = False
		self.reload_mode_text = ''
		self.current_language_text = self.__texts[self.__setting.language_id]

		self.set_text(self.current_language_text)
		self.set_color(self.__theme.sub_background_color)

		self.clicked.connect(self.__dropdown)
		logging.info('Виджет "LanguageDropdown": Инициализация завершена')

	def __dropdown(self):
		logging.info('Раскрытие списка языков "LanguageDropdown"')
		if self.reload_mode_flag:
			if self.__drop_thread and not isdeleted(self.__drop_thread) and self.__drop_thread.isRunning():
				self.__drop_worker.stop()
			self.set_text(text=self.current_language_text)
			self.__hide_language_subbutton()
			self.reload_mode_flag = False
			return
		
		self.__drop_thread = QThread()
		self.__drop_worker = TimerWorker(language_count=len(self.__texts))
		self.__drop_worker.moveToThread(self.__drop_thread)
		
		self.__drop_thread.started.connect(self.__drop_worker.run)
		self.__drop_worker.spawn_button_signal.connect(self.__show_language_subbutton)
		
		self.__drop_worker.finished.connect(self.__drop_thread.quit)
		self.__drop_worker.finished.connect(self.__drop_worker.deleteLater)
		self.__drop_thread.finished.connect(self.__drop_thread.deleteLater)
		
		self.__drop_thread.destroyed.connect(self.__clear_thread_references)
		
		self.reload_mode_flag = True
		self.set_text(text=self.reload_mode_text)
		self.__drop_thread.start()

	def __show_language_subbutton(self, index: int):
		current_geo = self.geometry()
		new_x = current_geo.x()
		new_y = current_geo.y() - (index + 1) * (current_geo.width() + self.__coordinate.header_theme_btn_offset)
		
		new_btn = LanguageSubButton(language_id=index,
		                            width=self.__width,
		                            height=self.__height,
		                            radius=self.radius,
									language_button=self,
									parent=self.parentWidget())
		new_btn.set_text(self.__texts[index])
		new_btn.set_color(self.__theme.sub_background_color)
		new_btn.setGeometry(new_x, new_y, self.__width, self.__height)
		new_btn.raise_()
		new_btn.show()
		
		self.__spawned_btn[index] = new_btn

	def __hide_language_subbutton(self):
		for key in list(self.__spawned_btn.keys()):
			self.__spawned_btn[key].hide()
			self.__spawned_btn[key].deleteLater()
			del self.__spawned_btn[key]
		logging.info('Закрытие списка тем "LanguageDropdown"')

	def change_language(self, language_id: int):
		if self.__drop_thread and not isdeleted(self.__drop_thread) and self.__drop_thread.isRunning():
			self.__drop_worker.stop()

		self.__setting.language_id = language_id
		self.current_language_text = self.__texts[language_id]
		self.set_text(text=self.current_language_text)
		self.reload_mode_flag = False
		logging.info(f'Выбран язык {language_id}')
		self.__hide_language_subbutton()

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
