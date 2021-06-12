import os
import re
from typing import Any, Dict, List, Optional, Union, Tuple

from snake.utils import format_number


def get_episode_tag(number: Union[int, str], leading_zeroes: int = 2) -> str:
    return f"E{format_number(number, leading_zeroes=leading_zeroes)}"


def extract_episode_tag(filename: str, return_as_upper: bool = True) -> Tuple[Optional[str], Optional[str]]:
    """
    Can match (case insentive:

    ```
    s##e##
    s###e###
    s##e###
    ```

    :param filename:
    :param return_as_upper:
    :return:
    """
    filename = filename.lower()

    matches = re.findall(r".*(s\d\d\de\d\d\d).*", filename)

    if not matches:
        matches = re.findall(r".*(s\d\de\d\d\d).*", filename)

    if not matches:
        matches = re.findall(r".*(s\d\de\d\d).*", filename)

    if not matches:
        return None, None

    splitted_tag = matches[0].split('e')
    season_tag = splitted_tag[0].upper() if return_as_upper else splitted_tag[0]
    episode_tag = f"E{splitted_tag[1]}" if return_as_upper else f"e{splitted_tag[1]}"

    return season_tag, episode_tag


def get_season_tag(number: Union[int, str], leading_zeroes: int = 2) -> str:
    return f"S{format_number(number, leading_zeroes=leading_zeroes)}"