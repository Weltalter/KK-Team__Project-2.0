from dataclasses import dataclass
from datetime import date
from pathlib import Path
from Code.Utils.Constants.sample_block import GameStatus, GameCoopStatus


@dataclass
class GameSample:
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

    def __post_init__(self):
        self.genres = [] if self.genres is None else list(self.genres)
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
    