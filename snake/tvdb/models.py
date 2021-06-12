from dataclasses import dataclass
from typing import List

from snake.utils.tv import get_episode_tag, get_season_tag


class Episode:
    def __init__(self, no: int, season: int, title: str, description: str, imdb_id: int = 0):
        self.no = no
        self.season = season
        self.title = title
        self.description = description
        self.imdb_id = imdb_id

    @property
    def tag(self) -> str:
        return get_episode_tag(self.no)

    def __str__(self):
        return f"{get_season_tag(self.season)}{self.tag} - {self.title}"


class Season:
    def __init__(self, no: int, episodes: List[Episode] = None):
        self.no = no
        self.episodes = episodes or []

    @property
    def tag(self) -> str:
        return get_season_tag(self.no)

    @property
    def total_episodes(self) -> int:
        return len(self.episodes)


@dataclass
class Show:
    tvdb_id: int
    imdb_id: int
    name: str
    description: str
    total_seasons: int
    seasons: List[Season]
    total_episodes: int
