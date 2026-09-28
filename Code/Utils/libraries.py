import logging
from pathlib import Path
from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from Code.Utils.samples import *
from Code.Utils.Scripts.id_generator import IdGenerator


class LibrarySingletonMeta(ModelMetaclass):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super().__call__(*args, **kwargs)
		return cls._instances[cls]

class LibraryActions():
	__id_generator: IdGenerator = IdGenerator()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		object.__setattr__(self, 'is_changed', False)

	def export_data(self, file_path: str = None):
		if not getattr(self, 'is_changed', False):
			logging.info(f'Библиотека "{self.__class__.__name__}": Изменений нет, экспорт отменен')
			return
		
		if file_path is None:
			file_path = f'{self.__class__.__name__}.txt'
		
		logging.info(f'Библиотека "{self.__class__.__name__}": Экспорт данных в {file_path}...')
		json_data = self.model_dump_json()

		with open(file_path, "w", encoding="utf-8") as f:
			f.write(json_data)

		object.__setattr__(self, 'is_changed', False)
		logging.info(f'Библиотека "{self.__class__.__name__}": Экспорт данных завершен')

	def import_data(self, file_path: str = None):
		if file_path is None:
			file_path = f'{self.__class__.__name__}.txt'
		
		logging.info(f'Библиотека "{self.__class__.__name__}": Импорт данных из {file_path}...')
		
		path = Path(file_path)
		if not path.exists() or path.stat().st_size == 0:
			logging.info(f'Библиотека "{self.__class__.__name__}": Не найден файл для импорта')
			return None

		with open(file_path, "r", encoding="utf-8") as f:
			json_data = f.read()

		imported_library = self.model_validate_json(json_data)

		for sample in imported_library.objects.values():
			sample.bind_to_library(self.__class__)
			
		logging.info(f'Библиотека "{self.__class__.__name__}": Импорт данных завершен')
		return imported_library

	def add(self, sample: BaseSample):
		sample.sample_id = self.__id_generator.get_id()
		sample.bind_to_library(self.__class__)
		self.objects[sample.sample_id] = sample

		object.__setattr__(self, 'is_changed', True)

	def remove(self, sample_id: int):
		self.__id_generator.release_id(sample_id)
		removed = self.objects.pop(sample_id, None)
		if removed:
			object.__setattr__(self, 'is_changed', True)
		return removed

	def notify_changed(self):
		object.__setattr__(self, 'is_changed', True)

class ApplicationLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, ApplicationSample] = {}

class BookLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, BookSample] = {}

class GameLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, GameSample] = {}

class MedicineLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, MedicineSample] = {}

class MovieLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, MovieSample] = {}

class RecipeLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, RecipeSample] = {}

class WebsiteLibrary(BaseModel, LibraryActions, metaclass=LibrarySingletonMeta):
	objects: dict[int, WebsiteSample] = {}
