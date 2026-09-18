from dataclasses import dataclass
from pathlib import Path
from Code.Utils.Constants.sample_block import BookStatus


@dataclass
class BookSample:
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

    def __post_init__(self):
        self.authors = [] if self.authors is None else list(self.authors)
        self.genres = [] if self.genres is None else list(self.genres)
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
    