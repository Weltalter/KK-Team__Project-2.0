import logging
from PyQt6.QtCore import QTimer
from PyQt6.sip import isdeleted
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.theme import Clr
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.setting import Setting
from Code.Utils.Constants.icon import Icon
from Code.UI.Component.rounded_icon_button import RoundedIconButton


class ThemeSubButton(RoundedIconButton):
	def __init__(self, theme_id: int = 0, width: int = 20, height: int = 20, radius: int = 20, path_to_icon: str = None, theme_button=None, parent=None):
		super().__init__(width=width, height=height, radius=radius, path_to_icon=path_to_icon, parent=parent)
		self.id = theme_id
		self._theme_button = theme_button
		
		self.clicked.connect(self._pick_theme)

	def _pick_theme(self):
		self._theme_button.change_theme(self.id)

class ThemeDropdown(RoundedIconButton):
	def __init__(self, parent=None):
		logging.info('Виджет "ThemeDropdown": Инициализация...')
		self._coordinate = Coordinate()
		self._setting = Setting()
		self._icon = Icon()

		self._parent = parent
		self._width = MathScripts.coordinate_scaling(self._coordinate.header_theme_btn_width)[0]
		self._height = MathScripts.coordinate_scaling(self._coordinate.header_theme_btn_height)[0]
		self._radius = MathScripts.coordinate_scaling(self._coordinate.header_theme_btn_radius)[0]

		super().__init__(width=self._width, height=self._height, radius=self._radius, parent=self._parent)
		
		self._spawned_btn: dict[int, ThemeSubButton] = {}
		self._icons: dict[int, str] = {i: self._icon.i_themes[i] for i in range(len(self._icon.i_themes))}
		self.current_theme_icon = self._icons[self._setting.theme_id]

		self._reload_mode_flag = False
		self._reload_mode_icon = self._icon.i_reload
		
		self.clicked.connect(self._show_theme_subbutton)
		logging.info('Виджет "ThemeDropdown": Инициализация завершена')

	def _init_theme_subbutton(self):
		for index in list(self._icons.keys()):
			new_btn = ThemeSubButton(theme_id=index,
									 width=self._width,
									 height=self._height,
									 radius=self._radius,
									 theme_button=self,
									 parent=self._parent)
			new_btn.raise_()
			self._spawned_btn[index] = new_btn
			self._reposition_subbuttons()

	def _show_theme_subbutton(self):
		if self._reload_mode_flag:
			self._hide_theme_subbutton()
			self.setIcon(path_to_icon=self.current_theme_icon)
			return
		
		logging.info('Раскрытие списка тем "ThemeDropdown"')

		self._reload_mode_flag = True
		self.setIcon(path_to_icon=self._reload_mode_icon)

		delay_step = 150 // len(self._spawned_btn) if self._spawned_btn else 0
		for index, key in enumerate(list(self._spawned_btn.keys())):
			btn = self._spawned_btn[key]
			current_delay = index * delay_step
			
			QTimer.singleShot(current_delay, btn.show)

	def _hide_theme_subbutton(self):
		for key in list(self._spawned_btn.keys()):
			self._spawned_btn[key].hide()
		self._reload_mode_flag = False
		logging.info('Закрытие списка тем "ThemeDropdown"')

	def _reposition_subbuttons(self):
		current_geo = self.geometry()
		for index, btn in self._spawned_btn.items():
			new_x = current_geo.x() - (index + 1) * (current_geo.width() + self._coordinate.header_theme_btn_offset)
			new_y = current_geo.y()
			btn.setGeometry(new_x, new_y, self._width, self._height)

	def change_theme(self, theme_id: int):
		self._setting.theme_id = theme_id
		Clr.set_theme_id(theme_id)
		self.current_theme_icon = self._icons[theme_id]
		self.setIcon(path_to_icon=self.current_theme_icon)
		
		logging.info(f'Выбрана тема {theme_id}')
		self._hide_theme_subbutton()
	
	def showEvent(self, event):
		super().showEvent(event)
		self._init_theme_subbutton()
		self.setIcon(path_to_icon=self.current_theme_icon)
		for index in list(self._spawned_btn.keys()):
			self._spawned_btn[index].setIcon(path_to_icon=self._icons[index])

	def hideEvent(self, event):
		self._hide_theme_subbutton()
		self.setIcon(path_to_icon=self.current_theme_icon) 
		
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
