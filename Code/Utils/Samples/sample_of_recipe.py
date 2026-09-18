from datetime import time
from pathlib import Path
from pydantic import BaseModel, model_validator
from Code.Utils.Constants.sample_block import DishType


class RecipeSample(BaseModel):
	title: str = ''
	poster: Path = None
	ingredients: list = None
	dish_type: DishType = DishType.OTHER
	comment: str = ''
	preparation_steps: str = ''
	preparation_time: time = time()
	hashtags: list = None

	@model_validator(mode="after")
	def post_init_logic(self):
		self.ingredients = [] if self.ingredients is None else list(self.ingredients)
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)
		
		return self

class RecipeLibrary(BaseModel):
	object_list: list[RecipeSample]
