from enum import IntEnum, Enum, unique


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

@unique
class Month(IntEnum):
	JANUARY = 1
	FEBRUARY = 2
	MARCH = 3
	APRIL = 4
	MAY = 5
	JUNE = 6
	JULY = 7
	AUGUST = 8
	SEPTEMBER = 9
	OCTOBER = 10
	NOVEMBER = 11
	DECEMBER = 12

@unique
class ColorName(Enum):
	MAIN_BACKGROUND = 1
	SUB_BACKGROUND = 2
	ACCENT_BACKGROUND = 3
	MAIN_BORDER = 4
	FONT = 5

@unique
class FontName(Enum):
	SHANTELL_SANS = 1

@unique
class MenuId(IntEnum):
	MAIN = 0
	MOVIE = 1
	GAME = 2
	RECIPE = 3
	BOOK = 4
	MEDICINE = 5
	WEBSITE = 6
	APPLICATION = 7
	ACCOUNT = 8

@unique
class ElementViewMode(Enum):
	LIST = 0
	POSTER = 1
	INFO = 2

@unique
class FilterState(IntEnum):
	NEUTRAL = 0
	ENABLE = 1
	DISABLE = 2
