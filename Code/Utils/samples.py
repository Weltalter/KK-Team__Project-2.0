from pathlib import Path
from datetime import time, date
from abc import ABC, abstractmethod
from pydantic import BaseModel, model_validator
from typing_extensions import Self
from Code.Utils.Constants.enum import *


class BaseSample(BaseModel, ABC):
	sample_id: int = None
	@model_validator(mode="after")
	def _run_custom_validation(self) -> Self:
		self.post_init_logic()
		return self

	@abstractmethod
	def post_init_logic(self) -> None:
		pass

class ApplicationSample(BaseSample):
	title: str = ''
	description: str = ''
	hashtags: list = None

	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class BookSample(BaseSample):
	title: str = ''
	poster: Path = None
	annotation: str = ''
	authors: list = None
	pages: int = 0
	status: BookStatus = BookStatus.PLANNING
	rating: float = None
	comment: str = ''
	genres: list = None
	hashtags: list = None

	def post_init_logic(self):
		self.authors = [] if self.authors is None else list(self.authors)
		self.genres = [] if self.genres is None else list(self.genres)
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class GameSample(BaseSample):
	title: str = ''
	poster: Path = None
	description: str = ''
	release_date: date = date.min
	status: GameStatus = GameStatus.PLANNING
	coop_status: GameCoopStatus = GameCoopStatus.UNKNOWN
	rating: float = None
	comment: str = ''
	genres: list = None
	hashtags: list = None

	def post_init_logic(self):
		self.genres = [] if self.genres is None else list(self.genres)
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class MedicineSample(BaseSample):
	title: str = ''
	description: str = ''
	medicine_type: MedicineType = MedicineType.OTHER
	effect_size: MedicineEffectSize = MedicineEffectSize.MODERATE
	expiration_date: date = date.min
	is_stock: bool = True
	comment: str = ''
	instruction: str = ''
	hashtags: list = None

	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

class MovieSample(BaseSample):
	title: str = ''
	poster: Path = None
	description: str = ''
	duration: time = time()
	release_date: date = date.min
	actors: list = None
	directors: list = None
	status: MovieStatus = MovieStatus.PLANNING
	rating: float = None
	comment: str = ''
	genres: list = None
	hashtags: list = None

	def post_init_logic(self):
		self.actors = [] if self.actors is None else list(self.actors)
		self.directors = [] if self.directors is None else list(self.directors)
		self.genres = [] if self.genres is None else list(self.genres)
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)

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

class WebsiteSample(BaseSample):
	title: str = ''
	url: str = ''
	description: str = ''
	vpn: bool = False
	hashtags: list = None

	def post_init_logic(self):
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)
