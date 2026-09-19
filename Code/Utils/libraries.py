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

	def export_data(self, file_name: str):
		json_data = self.model_dump_json()

		with open(file_name, "w", encoding="utf-8") as f:
			f.write(json_data)

	def import_data(self, file_name: str):
		path = Path(file_name)
		if not path.exists() or path.stat().st_size == 0:
			return None

		with open(file_name, "r", encoding="utf-8") as f:
			json_data = f.read()

		return self.model_validate_json(json_data)

	def add(self, sample: BaseSample):
		sample.sample_id = self.__id_generator.get_id()
		self.objects[sample.sample_id] = sample

	def remove(self, sample_id: int):
		self.__id_generator.release_id(sample_id)
		return self.objects.pop(sample_id, None)

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
