from enum import Enum, unique
from abc import ABC, abstractmethod
from pydantic import BaseModel, model_validator
from typing_extensions import Self


class BaseSample(BaseModel, ABC):
	@model_validator(mode="after")
	def _run_custom_validation(self) -> Self:
		self.post_init_logic()
		return self

	@abstractmethod
	def post_init_logic(self) -> None:
		pass

class BaseLibrary(BaseModel, ABC):
	object_list: list

@unique
class MovieStatus(Enum):
	WATCHED = 1
	NOT_RELEASED = 2
	PLANNING = 3

@unique
class GameStatus(Enum):
	PLAYED = 1
	NOT_RELEASED = 2
	PLANNING = 3

@unique
class GameCoopStatus(Enum):
	UNKNOWN = 1
	SOLO = 2
	TWO_P = 3
	THREE_P = 4
	FOUR_P = 5
	MORE = 6

@unique
class DishType(Enum):
	OTHER = 1
	FIRST_COURSE = 2
	SECOND_COURSE = 3
	SAUCE = 4
	DESSERT = 5
	BLANKET = 6
	SALAD = 7
	DRINK = 8

@unique
class MedicineType(Enum):
	OTHER = 1

@unique
class MedicineEffectSize(Enum):
	WEAK = 1
	MODERATE = 2
	STRONG = 3

@unique
class BookStatus(Enum):
	READED = 1
	NOT_RELEASED = 2
	PLANNING = 3
	READING = 4