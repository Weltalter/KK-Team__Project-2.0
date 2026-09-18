from abc import ABC
from pydantic import BaseModel
from Code.Utils.Patterns.singleton_meta import MetaSingleton
from Code.Utils.samples import *


class BaseLibrary(MetaSingleton, BaseModel, ABC):
	object_list: list

class ApplicationLibrary(BaseLibrary):
	object_list: list[ApplicationSample]

class BookLibrary(BaseLibrary):
	object_list: list[BookSample]

class GameLibrary(BaseLibrary):
	object_list: list[GameSample]

class MedicineLibrary(BaseLibrary):
	object_list: list[MedicineSample]

class MovieLibrary(BaseLibrary):
	object_list: list[MovieSample]

class RecipeLibrary(BaseLibrary):
	object_list: list[RecipeSample]

class WebsiteLibrary(BaseLibrary):
	object_list: list[WebsiteSample]
