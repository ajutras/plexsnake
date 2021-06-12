from typing import Any, Dict, List, Optional, Union, Tuple

from snake.constants import WINDOWS_ILLEGAL_CHARACTERS


def format_number(number: Union[int, str], leading_zeroes: int = 2) -> str:
    return f"{number:0{leading_zeroes}d}"


def slug_name_for_windows(name: str) -> str:
    slugged_name = name.strip()

    for illegal_character in WINDOWS_ILLEGAL_CHARACTERS:
        slugged_name = slugged_name.replace(illegal_character, '')

    return slugged_name


def split_filename_ext(filename_raw: str, lower_extension: bool = False) -> Tuple[str, Optional[str]]:
    splitted_parts = filename_raw.rsplit('.', maxsplit=1)
    filename = splitted_parts[0]
    extension = None

    if len(splitted_parts) > 1:
        extension = splitted_parts[1].lower() if lower_extension else splitted_parts[1]

    return filename, extension

