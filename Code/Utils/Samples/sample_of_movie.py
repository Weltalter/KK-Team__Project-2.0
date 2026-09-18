from datetime import time, date
from pathlib import Path
from Code.Utils.Constants.sample_block import BaseLibrary, BaseSample, MovieStatus


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

class MovieLibrary(BaseLibrary):
	object_list: list[MovieSample]
