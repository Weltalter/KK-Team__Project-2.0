from dataclasses import dataclass
import copy


@dataclass
class ApplicationSample:
    title: str = ''
    description: str = ''
    hashtags: list = None

    def __post_init__(self):
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)