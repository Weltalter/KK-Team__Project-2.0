from dataclasses import dataclass


@dataclass
class MovieSample:
    title: str = ''
    url: str = ''
    description: str = ''
    vpn: bool = False
    hashtags: list = None

    def __post_init__(self):
        self.hashtags = [] if self.hashtags is None else list(self.hashtags)
    