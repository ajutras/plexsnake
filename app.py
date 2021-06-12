import logging
from datetime import datetime
from typing import Dict, List, Union

import typer
from opset import setup_config, config
from plexapi.library import MovieSection, ShowSection
from plexapi.video import Season, Movie

from snake.constants import Operator
from snake.plex import plexcodex
from snake.utils import chronos
from snake.plex import models as plex_models  # noqa


log = logging.getLogger(__name__)

plexsnake_app = typer.Typer()


@plexsnake_app.command()
def list_added_videos(date: str):
    """
    Generate text that shows every movies or TV show added after the date specified, organized by library. TV Shows
    will be separated by seasons. By default will respect your list of whitelisted libraries, if you don't have any
    whitelisted libraries it will simply use all your libraries. This use the `addedAt` property in Plex. Output as
    text in terminal.

    :param date: A YYYY-MM-DD date, all videos added at this date or after will show up in the output.
    """

    libraries = plexcodex.list_libraries(filter_type=[ShowSection, MovieSection])  # Get all sections
    date = datetime.combine(chronos.parse_date(date), datetime.min.time())

    # Get all movies & TV shows by libraries
    new_videos: Dict[str, List[Union[Season, Movie]]] = {}
    advanced_filter = {"attribute": "addedAt", "operator": Operator.gte, "value": date}

    for library in libraries:
        if isinstance(library, ShowSection):
            new_videos[library.title] = plexcodex.list_seasons(library, advanced_filters=[advanced_filter])
        elif isinstance(library, MovieSection):
            new_videos[library.title] = plexcodex.list_movies(library, advanced_filters=[advanced_filter])

    # Display
    typer.secho(f"\nList of videos added at or after {date.date().isoformat()}\n", fg="blue")
    for library_name, videos in new_videos.items():
        if not videos:
            continue
        typer.secho(f"{library_name} ({len(videos)})", fg="blue")
        video_names = [str(video) for video in videos]
        video_names.sort()
        for video_name in video_names:
            typer.secho(f"  - {video_name}")
        print("\n")


@plexsnake_app.command()
def list_multiple_files():
    """
    List any TV shows or movies that resolve to more than one file. This command is useful to find potential issues
    from Plex in resolution of which files goes to what. Basically whenever plex offer you different versions of a
    video, it will be returned by this script.
    """

    libraries = plexcodex.list_libraries(filter_type=[ShowSection, MovieSection])
    for library in libraries:
        seasons = plexcodex.list_seasons(library)
        for season in seasons:
            for episode in season:
                if len(episode.locations) > 1:
                    typer.secho(f"\nPotential issue with [{season}]", fg="red")
                    for location in episode.locations:
                        typer.secho(f"  - {location}", fg="yellow")
                    print("")


if __name__ == "__main__":
    setup_config("plexsnake", "snake.config", setup_logging=True)
    plexsnake_app()
