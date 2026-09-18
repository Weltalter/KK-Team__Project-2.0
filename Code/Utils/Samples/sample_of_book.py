from pathlib import Path
from pydantic import BaseModel, model_validator
from Code.Utils.Constants.sample_block import BookStatus


class BookSample(BaseModel):
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

    @model_validator(mode="after")
    def post_init_logic(self):
        self.authors = [] if self.authors is None else list(self.authors)
        self.genres = [] if self.genres is None else list(self.genres)
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
        
        return self
    
class BookLibrary(BaseModel):
    object_list: list[BookSample]
    