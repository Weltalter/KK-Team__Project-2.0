import logging
from PyQt6.QtCore import QTimer
from PyQt6.sip import isdeleted
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.rounded_icon_button import RoundedIconButton


class ThemeSubButton(RoundedIconButton):
	def __init__(self, theme_id: int = 0, width: int = 20, height: int = 20, radius: int = 20, path_to_icon: str = None, theme_button=None, parent=None):
		super().__init__(width=width, height=height, radius=radius, path_to_icon=path_to_icon, parent=parent)
		self.id = theme_id
		self.__theme_button = theme_button
		
		self.clicked.connect(self.__pick_theme)

	def __pick_theme(self):
		self.__theme_button.change_theme(self.id)

class ThemeDropdown(RoundedIconButton):
	def __init__(self, parent=None):
		logging.info('Виджет "ThemeDropdown": Инициализация...')
		self.__coordinate = Coordinate()
		self.__setting = Setting()
		self.__icon = Icon()

		self.__parent = parent
		self.__width = MathScripts.coordinate_scaling(self.__coordinate.header_theme_btn_width)[0]
		self.__height = MathScripts.coordinate_scaling(self.__coordinate.header_theme_btn_height)[0]
		self.__radius = MathScripts.coordinate_scaling(self.__coordinate.header_theme_btn_radius)[0]

		super().__init__(width=self.__width, height=self.__height, radius=self.__radius, parent=self.__parent)
		
		self.__spawned_btn: dict[int, ThemeSubButton] = {}
		self.__icons: dict[int, str] = {i: self.__icon.i_themes[i] for i in range(len(self.__icon.i_themes))}
		self.current_theme_icon = self.__icons[self.__setting.theme_id]

		self.__reload_mode_flag = False
		self.__reload_mode_icon = self.__icon.i_reload
		
		self.__init_subbutton_flag = False

		self.setIcon(path_to_icon=self.current_theme_icon)

		self.clicked.connect(self.__show_theme_subbutton)
		logging.info('Виджет "ThemeDropdown": Инициализация завершена')

	def __init_theme_subbutton(self):
		for index in list(self.__icons.keys()):
			current_geo = self.geometry()
			new_x = current_geo.x() - (index + 1) * (current_geo.width() + self.__coordinate.header_theme_btn_offset)
			new_y = current_geo.y()
			
			new_btn = ThemeSubButton(theme_id=index,
			                         width=self.__width,
									 height=self.__height,
									 radius=self.__radius,
									 path_to_icon=self.__icons[index],
									 theme_button=self,
									 parent=self.__parent)
			new_btn.setGeometry(new_x, new_y, self.__width, self.__height)
			new_btn.raise_()
			
			self.__spawned_btn[index] = new_btn

	def __show_theme_subbutton(self):
		if not self.__init_subbutton_flag:
			self.__init_theme_subbutton()
			self.__init_subbutton_flag = True

		if self.__reload_mode_flag:
			self.__hide_theme_subbutton()
			self.setIcon(path_to_icon=self.current_theme_icon)
			return
		
		logging.info('Раскрытие списка тем "ThemeDropdown"')

		self.__reload_mode_flag = True
		self.setIcon(path_to_icon=self.__reload_mode_icon)

		delay_step = 150 // len(self.__spawned_btn) if self.__spawned_btn else 0
		for index, key in enumerate(list(self.__spawned_btn.keys())):
			btn = self.__spawned_btn[key]
			current_delay = index * delay_step
			
			QTimer.singleShot(current_delay, btn.show)

	def __hide_theme_subbutton(self):
		for key in list(self.__spawned_btn.keys()):
			self.__spawned_btn[key].hide()
		self.__reload_mode_flag = False
		logging.info('Закрытие списка тем "ThemeDropdown"')

	def change_theme(self, theme_id: int):
		self.__setting.theme_id = theme_id
		self.current_theme_icon = self.__icons[theme_id]
		self.setIcon(path_to_icon=self.current_theme_icon)
		
		logging.info(f'Выбрана тема {theme_id}')
		self.__hide_theme_subbutton()

	def destroy(self, destroyWindow=True, destroySubWindows=True):
		self.__stop_spawn_process()
		for btn in list(self.__spawned_btn.values()):
			if not isdeleted(btn):
				btn.deleteLater()
		self.__spawned_btn.clear()
		super().destroy(destroyWindow, destroySubWindows)
