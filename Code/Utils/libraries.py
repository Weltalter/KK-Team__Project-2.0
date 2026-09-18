from pydantic import BaseModel
from Code.Utils.samples import *


class ApplicationLibrary(BaseModel):
	object_list: list[ApplicationSample]

	_instances = {}
	
	def __call__(cls, *args, **kwargs):
		if cls._instances.get(cls) is None:
			cls._instances[cls] = super().__call__(*args, **kwargs)
		return cls._instances[cls]

	def __init__(self, **data):
		if not hasattr(self, "__pydantic_fields_set__") or not self.__pydantic_fields_set__:
			super().__init__()

class BookLibrary(BaseModel):
	object_list: list[BookSample]

class GameLibrary(BaseModel):
	object_list: list[GameSample]

class MedicineLibrary(BaseModel):
	object_list: list[MedicineSample]

class MovieLibrary(BaseModel):
	object_list: list[MovieSample]

class RecipeLibrary(BaseModel):
	object_list: list[RecipeSample]

class WebsiteLibrary(BaseModel):
	object_list: list[WebsiteSample]
