from datetime import time, date
from pathlib import Path
from pydantic import BaseModel, model_validator
from Code.Utils.Constants.sample_block import MovieStatus


class MovieSample(BaseModel):
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

    @model_validator(mode="after")
    def post_init_logic(self):
        self.actors = [] if self.actors is None else list(self.actors)
        self.directors = [] if self.directors is None else list(self.directors)
        self.genres = [] if self.genres is None else list(self.genres)
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
        
        return self

class MovieLibrary(BaseModel):
    object_list: list[MovieSample]
    