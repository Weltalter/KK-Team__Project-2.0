from datetime import date
from pathlib import Path
from pydantic import BaseModel, model_validator
from Code.Utils.Constants.sample_block import GameStatus, GameCoopStatus


class GameSample(BaseModel):
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

	@model_validator(mode="after")
	def post_init_logic(self):
		self.genres = [] if self.genres is None else list(self.genres)
		self.hashtags = [] if self.hashtags is None else list(self.hashtags)
		
		return self

class GameLibrary(BaseModel):
	object_list: list[GameSample]
