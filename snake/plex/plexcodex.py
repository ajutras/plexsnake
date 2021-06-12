import logging
from typing import Any, Dict, List, Union

from opset import config
from plexapi.library import MovieSection, MusicSection, PhotoSection, ShowSection
from plexapi.video import Movie, Season

from snake.constants import SECTION_TYPE, Operator
from snake.plex.client import get_plex_client

log = logging.getLogger(__name__)


def get_library(name: str) -> Union[MovieSection, ShowSection, MusicSection, PhotoSection]:
    plex_client = get_plex_client()
    section = plex_client.library.section(name)

    return section


def list_libraries(
    filter_type: Union[SECTION_TYPE, List[SECTION_TYPE]] = None, whitelisted_libraries: List[str] = None
) -> List[Union[MovieSection, ShowSection, MusicSection, PhotoSection]]:
    whitelisted_libraries = whitelisted_libraries or [ws for ws in config.whitelisted_libraries]

    filter_types = filter_type or []
    filter_types = filter_types if isinstance(filter_types, list) else [filter_types]

    log.info("Listing libraries..")

    plex_client = get_plex_client()
    libraries = plex_client.library.sections()

    # Keep only the type of libraries (like Movies, TV, Music, etc..) that we want
    filtered_libraries = []
    if filter_types:
        for library in libraries:
            if type(library) in filter_types:
                filtered_libraries.append(library)
    else:
        filtered_libraries = libraries

    # Apply whitelisting of libraries
    libraries = []
    for library in filtered_libraries:
        if whitelisted_libraries and library.title not in whitelisted_libraries:
            continue
        libraries.append(library)

    return libraries


def list_movies(
    movie_library: MovieSection,
    title: str = None,
    sort: str = None,
    max_results: int = None,
    advanced_filters: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    **kwargs,
) -> List[Movie]:
    """
    List movies from a MovieSection.

    :param movie_library: The MovieSection to search into.
    :param title: General string query to search for.
    :param sort: column:dir; column can be any of {addedAt, originallyAvailableAt, lastViewedAt, titleSort, rating,
        mediaHeight, duration}. dir can be asc or desc.
    :param max_results: Only return the specified number of results.
    :param advanced_filters: List of dicts with keys attribute, operator and value.
    :param kwargs:
        * unwatched: Display or hide unwatched content (True, False). [all]
        * duplicate: Display or hide duplicate items (True, False). [movie]
        * actor: List of actors to search ([actor_or_id, ...]). [movie]
        * collection: List of collections to search within ([collection_or_id, ...]). [all]
        * contentRating: List of content ratings to search within ([rating_or_key, ...]). [movie,tv]
        * country: List of countries to search within ([country_or_key, ...]). [movie,music]
        * decade: List of decades to search within ([yyy0, ...]). [movie]
        * director: List of directors to search ([director_or_id, ...]). [movie]
        * genre: List Genres to search within ([genre_or_id, ...]). [all]
        * network: List of TV networks to search within ([resolution_or_key, ...]). [tv]
        * resolution: List of video resolutions to search within ([resolution_or_key, ...]). [movie]
        * studio: List of studios to search within ([studio_or_key, ...]). [music]
        * year: List of years to search within ([yyyy, ...]). [all]

    :return:
        A list of movies fitting the criteria.
    """
    advanced_filters = advanced_filters or []
    advanced_filters = advanced_filters if isinstance(advanced_filters, list) else [advanced_filters]
    movies = []

    log.info(f"Searching into library [{movie_library.title}]..")

    for movie in movie_library.search(title=title, sort=sort, maxresults=max_results, **kwargs):
        skip: bool = False
        for advanced_filter in advanced_filters:
            movie_value = getattr(movie, advanced_filter["attribute"])
            value = advanced_filter["value"]
            if advanced_filter["operator"] == Operator.eq and value != movie_value:
                skip = True
            elif advanced_filter["operator"] == Operator.in_ and value not in movie_value:
                skip = True
            elif advanced_filter["operator"] == Operator.gt and value > movie_value:
                skip = True
            elif advanced_filter["operator"] == Operator.lt and value < movie_value:
                skip = True
            elif advanced_filter["operator"] == Operator.gte and value >= movie_value:
                skip = True
            elif advanced_filter["operator"] == Operator.lte and value <= movie_value:
                skip = True

        if skip:
            continue

        movies.append(movie)

    return movies


def list_seasons(
    show_library: ShowSection,
    title: str = None,
    sort: str = None,
    max_results: int = None,
    advanced_filters: Union[Dict[str, Any], List[Dict[str, Any]]] = None,
    **kwargs,
) -> List[Season]:
    """
    List tv show seasons from a TV show library.

    :param show_library: The ShowSection to search into.
    :param title: General string query to search for.
    :param sort: column:dir; column can be any of {addedAt, originallyAvailableAt, lastViewedAt, titleSort, rating,
        mediaHeight, duration}. dir can be asc or desc.
    :param max_results: Only return the specified number of results.
    :param advanced_filters: List of dicts with keys attribute, operator and value.
    :param kwargs:

    :return:
        A list of movies fitting the criteria.
    """
    advanced_filters = advanced_filters or []
    advanced_filters = advanced_filters if isinstance(advanced_filters, list) else [advanced_filters]
    seasons = []

    log.info(f"Searching into library [{show_library.title}]..")

    for show in show_library.search(title=title, sort=sort, maxresults=max_results, **kwargs):
        for season in show:

            skip: bool = False
            for advanced_filter in advanced_filters:
                season_value = getattr(season, advanced_filter["attribute"])
                value = advanced_filter["value"]
                if advanced_filter["operator"] == Operator.eq and value != season_value:
                    skip = True
                elif advanced_filter["operator"] == Operator.in_ and value not in season_value:
                    skip = True
                elif advanced_filter["operator"] == Operator.gt and value > season_value:
                    skip = True
                elif advanced_filter["operator"] == Operator.lt and value < season_value:
                    skip = True
                elif advanced_filter["operator"] == Operator.gte and value >= season_value:
                    skip = True
                elif advanced_filter["operator"] == Operator.lte and value <= season_value:
                    skip = True

            if skip:
                continue

            seasons.append(season)

    return seasons
