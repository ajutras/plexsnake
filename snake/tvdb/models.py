from dataclasses import dataclass
from typing import Dict, List, Optional, Union

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


class Proposal:
    def __init__(self, path: str, origin_file_list: List[List[str]], proposal_file_list: List[List[str]] = None,
                 encoding: str = None, season_no: Union[int, str] = None, show: Show = None):
        """

        :param origin_file_list:
        :param proposal_file_list:
        :param encoding:
        :param season_no:
        :param show:

        """
        self.path = path
        self.origin_file_list = origin_file_list
        self.proposal_file_list = proposal_file_list or []
        self.encoding = encoding
        self.season_no = season_no
        self.show: Show = show


@dataclass
class Default:
    _: bool = None
