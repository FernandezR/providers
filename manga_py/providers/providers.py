from typing import List

from ._providers.readmanga_me import ReadMangaMe
from .exceptions import ProviderNotFoundError

_providers = [
    ReadMangaMe,
]


def matched_providers(url: str) -> List:
    """
    Returns a list of provider instances
    """
    providers = [p for p in _providers if p.is_supported(url)]

    if len(providers) < 1:
        raise ProviderNotFoundError()

    return providers


__all__ = ['matched_providers']
