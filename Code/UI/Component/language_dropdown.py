import logging
from PyQt6.QtCore import QTimer
from PyQt6.sip import isdeleted
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.theme import Clr
from Code.UI.Component.CommonWidget.rounded_text_button import RoundedTextButton


class LanguageSubButton(RoundedTextButton):
	def __init__(self, language_id: int = 0, width: int = 20, height: int = 20, radius: int = 20, language_button=None, parent=None):
		super().__init__(width=width, height=height, radius=radius, border_flag=True, parent=parent)
		self.id = language_id
		self._language_button = language_button
		
		self.clicked.connect(self._pick_language)

	def _pick_language(self):
		self._language_button.change_language(self.id)

class LanguageDropdown(RoundedTextButton):
	def __init__(self, parent=None):
		logging.info('Виджет "LanguageDropdown": Инициализация...')
		self._coordinate = Coordinate()
		self._setting = Setting()
		self._message = Message()

		self._parent = parent
		self._width = MathScripts.coordinate_scaling(self._coordinate.footer_language_btn_width)[0]
		self._height = MathScripts.coordinate_scaling(self._coordinate.footer_language_btn_height)[0]
		self._radius = MathScripts.coordinate_scaling(self._coordinate.footer_language_btn_radius)[0]

		super().__init__(width=self._width, height=self._height, radius=self._radius, border_flag=True, parent=self._parent)

		self._spawned_btn: dict[int, LanguageSubButton] = {}
		self._texts: dict[int, str] = {i: self._message.m_languages[i] for i in range(len(self._message.m_languages))}
		self.current_language_text = self._texts[self._setting.language_id]

		self._reload_mode_flag = False
		self._reload_mode_text = ''

		self.clicked.connect(self._show_language_subbutton)
		logging.info('Виджет "LanguageDropdown": Инициализация завершена')

	def _init_language_subbutton(self):
		for index in list(self._texts.keys()):
			new_btn = LanguageSubButton(language_id=index,
										width=self._width,
										height=self._height,
										radius=self._radius,
										language_button=self,
										parent=self._parent)
			new_btn.set_text(self._texts[index])
			new_btn.raise_()
			self._spawned_btn[index] = new_btn
			self._reposition_subbuttons()

	def _show_language_subbutton(self):
		if self._reload_mode_flag:
			self._hide_language_subbutton()
			self.set_text(text=self.current_language_text)
			return
		
		logging.info('Раскрытие списка языков "LanguageDropdown"')

		self._reload_mode_flag = True
		self.set_text(text=self._reload_mode_text)

		delay_step = 150 // len(self._spawned_btn) if self._spawned_btn else 0
		for index, key in enumerate(list(self._spawned_btn.keys())):
			btn = self._spawned_btn[key]
			current_delay = index * delay_step
			
			QTimer.singleShot(current_delay, btn.show)

	def _hide_language_subbutton(self):
		for key in list(self._spawned_btn.keys()):
			self._spawned_btn[key].hide()
		self._reload_mode_flag = False
		logging.info('Закрытие списка тем "LanguageDropdown"')

	def _reposition_subbuttons(self):
		current_geo = self.geometry()
		for index, btn in self._spawned_btn.items():
			new_x = current_geo.x() + (index + 1) * (current_geo.width() + self._coordinate.footer_language_btn_offset)
			new_y = current_geo.y()
			btn.setGeometry(new_x, new_y, self._width, self._height)

	def change_language(self, language_id: int):
		self._setting.language_id = language_id
		self.current_language_text = self._texts[language_id]
		self.set_text(text=self.current_language_text)

		logging.info(f'Выбран язык {language_id}')
		self._hide_language_subbutton()

	def update_theme(self):
		self.set_color(Clr.sub_bg())
		for btn in list(self._spawned_btn.values()):
			btn.set_color(Clr.sub_bg())
	
	def showEvent(self, event):
		super().showEvent(event)
		self._init_language_subbutton()
		self.set_text(self.current_language_text)
		self.update_theme()
		Clr.subscribe(self.update_theme)

	def hideEvent(self, event):
		self._hide_language_subbutton()
		self.set_text(text=self.current_language_text)
		
		super().hideEvent(event)

	def moveEvent(self, event):
		super().moveEvent(event)
		self._reposition_subbuttons()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self._reposition_subbuttons()
	
	def destroy(self, destroyWindow=True, destroySubWindows=True):
		self._stop_spawn_process()
		for btn in list(self._spawned_btn.values()):
			if not isdeleted(btn):
				btn.deleteLater()
		self._spawned_btn.clear()
		super().destroy(destroyWindow, destroySubWindows)
