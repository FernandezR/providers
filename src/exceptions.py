from .types import *
from requests import Response

__all__ = [
    'InfoException',
    'SiteDownException',
    'ChaptersNotFoundException',
    'ImagesNotFoundException',
    'CoverNotFoundException',
    'ImageSrcAttrEmptyException',
    'ProviderError',
    'WrongResponseException',
    'BackgroundImageExtractException',
    'CantWriteFileException',
    'WarningException',
]


# Base exceptions
class FatalException(Exception):
    """ Fatal exceptions. Can't be continue """
    pass


class ErrorException(Exception):
    """ Error exceptions. Can't be continue """
    pass


class InfoException(UserWarning):
    """ Log only """
    pass


class WarningException(Warning):
    """ Can be continue"""
    pass


# Fatal exceptions
class SiteDownException(FatalException):
    pass


# Not found exceptions
class ChaptersNotFoundException(InfoException):
    def __init__(self, chapter: Chapter):
        self.chapter = chapter


class ImagesNotFoundException(InfoException):
    def __init__(self, chapter: Chapter):
        self.chapter = chapter


class CoverNotFoundException(InfoException):
    def __init__(self, cover_url: str = None):
        self.cover_url = cover_url


# other warning exceptions
class ImageSrcAttrEmptyException(WarningException):
    def __init__(self, chapter: Chapter, image: Image):
        self.chapter = chapter
        self.image = image


class WrongResponseException(WarningException):
    def __init__(self, response: Response):
        self.response = response


class BackgroundImageExtractException(WarningException):
    def __init__(self, style: str):
        self.style = style


class CantWriteFileException(WarningException):
    def __init__(self, path: str):
        self.path = path


# Provider internal errors
class ProviderError(ErrorException):
    pass


# Info exceptions
