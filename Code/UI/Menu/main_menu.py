from PyQt6.QtWidgets import (
	QWidget,
	QVBoxLayout,
	QHBoxLayout,
	QLabel,
)
from Code.Utils.Scripts.math_scripts import MathScripts
from Code.Utils.Constants.coordinate import Coordinate
from Code.Utils.Constants.theme import Clr, Fnt
from Code.Utils.Constants.message import Message
from Code.UI.Component.theme_dropdown import ThemeDropdown
from Code.UI.Component.language_dropdown import LanguageDropdown
from Code.UI.Component.main_menu_scroll_area import MainMenuScrollArea


class MainMenu(QWidget):
	def __init__(self, manager):
		self.manager = manager
		super().__init__()
		self._coordinate = Coordinate()
		self._message = Message()
		
		#region ПРОМЕЖУТОЧНЫЙ LAYOUT (Для разделения на основной контент и низ)
		body_layout = QVBoxLayout(self)
		body_layout.setSpacing(0)
		body_layout.setContentsMargins(0, 0, 0, 0)
		#endregion

		#region СЕКТОР 2: Верхняя панель (Header)
		header_widget = QWidget()
		header_widget.setObjectName("Header")
		header_widget.setFixedHeight(*MathScripts.coordinate_scaling(self._coordinate.header_height)) 

		header_layout = QHBoxLayout(header_widget)
		
		padding = MathScripts.coordinate_scaling(self._coordinate.header_padding)[0]
		header_layout.setContentsMargins(padding, padding, padding, padding)
		header_layout.setSpacing(0)
		
		btn_theme = ThemeDropdown(parent=header_widget)

		header_layout.addStretch()
		header_layout.addWidget(btn_theme)
		
		body_layout.addWidget(header_widget)
		#endregion

		#region СЕКТОР 3: Главный контент (Main Content)
		content_widget = QWidget()
		content_widget.setObjectName("Content")

		content_layout = QHBoxLayout(content_widget)
		
		# ========================================================
		# 1. ЗАДАЕМ ОТСТУПЫ 40 ПИКСЕЛЕЙ ОТ КРАЕВ С УЧЕТОМ МАСШТАБА
		# ========================================================
		content_margin = MathScripts.coordinate_scaling(self._coordinate.main_menu_margin)[0]
		content_layout.setContentsMargins(content_margin, content_margin, content_margin, content_margin)
		content_layout.setSpacing(0)

		# Создаем QScrollArea (область прокрутки)
		sidebar_expand_w = MathScripts.coordinate_scaling(self._coordinate.sidebar_expanded_width)[0]
		mm_scroll_area_width = self.manager.get_screen_geometry().width() - sidebar_expand_w - 2*content_margin
		mm_scroll_area = MainMenuScrollArea(width=mm_scroll_area_width, manager=self.manager, parent=content_widget)
		content_layout.addWidget(mm_scroll_area)
		
		body_layout.addWidget(content_widget)
		#endregion

		#region СЕКТОР 4: Нижняя панель (Footer)
		footer_widget = QWidget()
		footer_widget.setObjectName("Footer")
		footer_widget.setFixedHeight(*MathScripts.coordinate_scaling(self._coordinate.footer_height))

		footer_layout = QHBoxLayout(footer_widget)

		padding = MathScripts.coordinate_scaling(self._coordinate.footer_padding)[0]
		footer_layout.setContentsMargins(padding, padding, padding, padding)
		footer_layout.setSpacing(0)

		creator_lbl = QLabel(self._message.m_version)
		creator_lbl.setObjectName("VersionLabel")
		creator_lbl.setFont(Fnt.shantell_sans(14))
		
		btn_language = LanguageDropdown(parent=footer_widget)

		footer_layout.addWidget(btn_language)
		footer_layout.addStretch()
		footer_layout.addWidget(creator_lbl)

		body_layout.addWidget(footer_widget)
		#endregion

	def update_theme(self):
		self.setStyleSheet(f'''
			#Header {{
				background-color: {Clr.main_bg()};
			}}
			#Content {{
				background-color: {Clr.main_bg()};
			}}
			#Footer {{
				background-color: {Clr.main_bg()};
			}}
			#VersionLabel {{
				color: {Clr.font()};
			}}
		''')

	def showEvent(self, event):
		super().showEvent(event)
		self.update_theme()
		Clr.subscribe(self.update_theme)
	