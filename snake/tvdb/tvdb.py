import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Union

import requests
from opset import config

from snake.tvdb.models import Episode, Season, Show


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

current_token: Optional[str] = None
token_creation_time: Optional[datetime] = None
fed_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODAxMDI3MDQsImlkIjoiSGl0cmVuYW1lciIsIm9yaWdfaWF0IjoxNTc5NDk3OTA0LCJ1c2VyaWQiOjIyNTAyMTAsInVzZXJuYW1lIjoiZmxhcHBlciJ9.apfgC5MA0vvjZOvtPsIHJR7bBWP6GR79OUupCvUbd4bq04-2M4ASkJ9Y_hfxAqoXWzEA1m0j8wf9GyGuR-M9l6o-udmTwgAkRQ57_qBeflHTBpZ7sbe2Ufi3LGb-U_l7gp352H_Eik4C2YvizbTcq_zNnkapnaC-5yfg7nn29FEJgs7Xs7R5k5qcyqYQzMyLGhydBMUvBpT5jip0wL0z4a4rFnmB4IX2ZFQaowZ5ib_sVknQ89-ZGvgaJ8wNyfJtipCGKF8y_sXMsBDUnanmwzsvy65fvwfmBVCcHM4zd6amvakaaJdxq9xIAu5l6OBiVnBleq-ZCl-ZyWT0l_izHg"
fed_token_creation_time = datetime.now(tz=timezone.utc)


def has_token_expired() -> bool:
    global current_token
    global token_creation_time

    if not token_creation_time or not current_token:
        return True

    now = datetime.now(tz=timezone.utc)
    expiration_time = timedelta(hours=23)
    token_age = now - token_creation_time

    has_expired = token_age > expiration_time

    if has_expired:
        log.info(f"The TVDB API token has expired, the token was {getattr(token_age, 'hour', '???')} hours old.")

    return has_expired


def get_token() -> str:
    global current_token
    global token_creation_time

    if has_token_expired():
        logging.info("Acquiring new TVDB API token")
        current_token = auth()
        token_creation_time = datetime.now(tz=timezone.utc)
        logging.info(f"Token acquired {current_token} at {token_creation_time.isoformat()}")

    return current_token


def get_headers() -> Dict:
    global fed_token
    global current_token
    global token_creation_time
    global fed_token_creation_time
    if fed_token:
        current_token = fed_token
        token_creation_time = fed_token_creation_time
    token = get_token()
    return {"Accept": "application/json", "Authorization": f"Bearer {token}"}


def auth() -> str:
    """Get TVDB API Token."""
    result = requests.post(f"{config.tvdb.host}/login",
                           json={
                               "apikey": config.tvdb.api_key,
                               "username": config.tvdb.user,
                               "userkey": config.tvdb.userkey
                           }, timeout=20)
    result.raise_for_status()

    auth_answer = result.json()

    return auth_answer["token"]


def refresh_token() -> str:
    result = requests.get(f"{config.tvdb.host}/refresh_token", headers=get_headers(), timeout=10)
    result.raise_for_status()

    return result.json()["token"]


def get_episodes_raw(show_id: int, page: int = 1) -> List[Dict]:
    result = requests.get(f"{config.tvdb.host}/series/{show_id}/episodes",
                          headers=get_headers(),
                          params={
                              "page": page
                          }, timeout=7)
    result.raise_for_status()

    return result.json()["data"]


def get_show_raw(show_id: Union[int, str]) -> Dict:
    result = requests.get(f"{config.tvdb.host}/series/{show_id}",
                          headers=get_headers(),
                          timeout=7)
    result.raise_for_status()

    return result.json()["data"]


def get_show(show_id: Union[int, str]) -> Show:
    show_raw = get_show_raw(show_id)

    return Show(
        tvdb_id=show_id,
        imdb_id=show_raw["imdbId"],
        name=show_raw["seriesName"],
        description="",
        total_seasons=show_raw["season"],
        seasons=get_seasons(show_id),
        total_episodes=0
    )


def get_seasons(show_id: Union[int, str]) -> List[Season]:
    all_done = False
    seasons = []
    episodes_raw = []

    # Get episodes
    i = 1
    while not all_done:
        try:
            result = get_episodes_raw(show_id=show_id, page=i)
        except Exception:
            log.exception("uh oh")
            raise
        episodes_raw = episodes_raw + result
        if len(result) < 100:
            all_done = True
        i += 1

    # Create seasons and episodes, associate them
    for episode in episodes_raw:
        season_no = episode["airedSeason"]
        episode_no = episode['airedEpisodeNumber']
        episode_title = episode["episodeName"]
        episode_description = episode["overview"]

        if season_no not in [season.no for season in seasons]:
            seasons.append(Season(no=season_no, episodes=[]))

        season = next((season for season in seasons if season.no == season_no))

        season.episodes.append(Episode(
            no=int(episode_no),
            season=int(season_no),
            title=episode_title or "",
            description=episode_description or ""
        ))

    # sort seasons
    seasons = sorted(seasons, key=lambda season: season.no)

    # sort episodes in each season
    for season in seasons:
        season.episodes = sorted(season.episodes, key=lambda episode: episode.no)

    return seasons
