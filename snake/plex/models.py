from plexapi.library import MovieSection, ShowSection
from plexapi.video import Movie, Season, Show

from snake.utils import format_number


def str_section(self):
    return f"{self.title}"


def str_video(self):
    return f"{self.title} ({self.year})"


def str_season(self):
    return f"{self.parentTitle} - Season {format_number(self.seasonNumber)}"


# Monkey patching some of the models from plexapi
ShowSection.__str__ = str_section
ShowSection.__repr__ = str_section
MovieSection.__str__ = str_section
MovieSection.__repr__ = str_section
Movie.__str__ = str_video
Movie.__repr__ = str_video
Show.__str__ = str_video
Show.__repr__ = str_video
Season.__str__ = str_season
Season.__repr__ = str_season
