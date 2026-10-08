import logging
from PyQt6.QtCore import QTimer
from PyQt6.sip import isdeleted
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.message import Message
from Code.Utils.Constants.theme import Theme
from Code.UI.Component.rounded_text_button import RoundedTextButton


class LanguageSubButton(RoundedTextButton):
	def __init__(self, language_id: int = 0, width: int = 20, height: int = 20, radius: int = 20, language_button=None, parent=None):
		super().__init__(width=width, height=height, radius=radius, parent=parent)
		self.id = language_id
		self.__language_button = language_button
		
		self.clicked.connect(self.__pick_language)

	def __pick_language(self):
		self.__language_button.change_language(self.id)

class LanguageDropdown(RoundedTextButton):
	def __init__(self, parent=None):
		logging.info('Виджет "LanguageDropdown": Инициализация...')
		self.__coordinate = Coordinate()
		self.__setting = Setting()
		self.__message = Message()
		self.__theme = Theme()

		self.__parent = parent
		self.__width = MathScripts.coordinate_scaling(self.__coordinate.footer_language_btn_width)[0]
		self.__height = MathScripts.coordinate_scaling(self.__coordinate.footer_language_btn_height)[0]
		self.__radius = MathScripts.coordinate_scaling(self.__coordinate.footer_language_btn_radius)[0]

		super().__init__(width=self.__width, height=self.__height, radius=self.__radius, parent=self.__parent)

		self.__spawned_btn: dict[int, LanguageSubButton] = {}
		self.__texts: dict[int, str] = {i: self.__message.m_languages[i] for i in range(len(self.__message.m_languages))}
		self.current_language_text = self.__texts[self.__setting.language_id]

		self.__reload_mode_flag = False
		self.__reload_mode_text = ''

		self.__init_subbutton_flag = False

		self.set_text(self.current_language_text)
		self.set_color(self.__theme.sub_background_color)

		self.clicked.connect(self.__show_language_subbutton)
		logging.info('Виджет "LanguageDropdown": Инициализация завершена')

	def __init_language_subbutton(self):
		for index in list(self.__texts.keys()):
			current_geo = self.geometry()
			new_x = current_geo.x() + (index + 1) * (current_geo.width() + self.__coordinate.footer_language_btn_offset)
			new_y = current_geo.y()
			
			new_btn = LanguageSubButton(language_id=index,
										width=self.__width,
										height=self.__height,
										radius=self.__radius,
										language_button=self,
										parent=self.__parent)
			new_btn.set_text(self.__texts[index])
			new_btn.set_color(self.__theme.sub_background_color)
			new_btn.setGeometry(new_x, new_y, self.__width, self.__height)
			new_btn.raise_()
			self.__spawned_btn[index] = new_btn

	def __show_language_subbutton(self):
		if not self.__init_subbutton_flag:
			self.__init_language_subbutton()
			self.__init_subbutton_flag = True

		if self.__reload_mode_flag:
			self.__hide_language_subbutton()
			self.set_text(text=self.current_language_text)
			return
		
		logging.info('Раскрытие списка языков "LanguageDropdown"')

		self.__reload_mode_flag = True
		self.set_text(text=self.__reload_mode_text)

		delay_step = 150 // len(self.__spawned_btn) if self.__spawned_btn else 0
		for index, key in enumerate(list(self.__spawned_btn.keys())):
			btn = self.__spawned_btn[key]
			current_delay = index * delay_step
			
			QTimer.singleShot(current_delay, btn.show)

	def __hide_language_subbutton(self):
		for key in list(self.__spawned_btn.keys()):
			self.__spawned_btn[key].hide()
		self.__reload_mode_flag = False
		logging.info('Закрытие списка тем "LanguageDropdown"')

	def change_language(self, language_id: int):
		self.__setting.language_id = language_id
		self.current_language_text = self.__texts[language_id]
		self.set_text(text=self.current_language_text)

		logging.info(f'Выбран язык {language_id}')
		self.__hide_language_subbutton()

	def destroy(self, destroyWindow=True, destroySubWindows=True):
		self.__stop_spawn_process()
		for btn in list(self.__spawned_btn.values()):
			if not isdeleted(btn):
				btn.deleteLater()
		self.__spawned_btn.clear()
		super().destroy(destroyWindow, destroySubWindows)
