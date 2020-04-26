from pathlib import Path
from sys import platform
from typing import Tuple

__all__ = ['sanitize_filename', ]

__is_win = platform == 'win32'

if __is_win:
    __illegal = ':<>|"?*\\/'
else:
    __illegal = '/'

_sanitize_table = str.maketrans(__illegal, '_' * len(__illegal))


def __get_parts(start: str, *other: str) -> Tuple[str, Tuple[str]]:
    return start, other


def sanitize_filename(name: str):
    """Replace bad characters and remove trailing dots from parts."""
    return name.translate(_sanitize_table)


def sanitize_full_path(path: Path):
    start, other_parts = __get_parts(*path.resolve().parts)

    if len(other_parts) == 0:
        return path

    sanitized = [sanitize_filename(part) for part in other_parts]
    return Path(start).joinpath(*sanitized)

