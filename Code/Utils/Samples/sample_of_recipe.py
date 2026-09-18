from datetime import time
from pathlib import Path
from Code.Utils.Constants.sample_block import BaseLibrary, BaseSample, DishType


class RecipeSample(BaseSample):
	title: str = ''
	poster: Path = None
	ingredients: list = None
	dish_type: DishType = DishType.OTHER
	comment: str = ''
	preparation_steps: str = ''
	preparation_time: time = time()
	hashtags: list = None

	def post_init_logic(self):
		self.ingredients = [] if self.ingredients is None else list(self.ingredients)
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class RecipeLibrary(BaseLibrary):
	object_list: list[RecipeSample]
