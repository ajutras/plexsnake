from typing import Union


def format_number(number: Union[int, str], leading_zeroes: int = 2) -> str:
    return f"{number:0{leading_zeroes}d}"
