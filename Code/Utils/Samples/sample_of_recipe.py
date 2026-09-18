from dataclasses import dataclass
from datetime import time
from pathlib import Path
from Code.Utils.Constants.sample_block import DishType


@dataclass
class GameSample:
    title: str = ''
    poster: Path = None
    ingredients: list = None
    dish_type: DishType = DishType.OTHER
    comment: str = ''
    preparation_steps: str = ''
    preparation_time: time = time()
    hashtags: list = None

    def __post_init__(self):
        self.ingredients = [] if self.ingredients is None else list(self.ingredients)
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
    