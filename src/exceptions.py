from .types import *
from urllib3 import HTTPResponse

__all__ = [
    'InfoException',
    'SiteDownException',
    'ChaptersNotFoundException',
    'ImagesNotFoundException',
    'CoverNotFoundException',
    'ImageSrcAttrEmptyException',
    'ProviderError',
    'WrongResponseException',
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
class ChaptersNotFoundException(WarningException):
    def __init__(self, chapter: Chapter):
        self.chapter = chapter


class ImagesNotFoundException(WarningException):
    def __init__(self, chapter: Chapter, image: Image):
        self.chapter = chapter
        self.image = image


class CoverNotFoundException(WarningException):
    def __init__(self, cover_url: str = None):
        self.cover_url = cover_url


class ImageSrcAttrEmptyException(WarningException):
    def __init__(self, chapter: Chapter, image: Image):
        self.chapter = chapter
        self.image = image


# Provider internal errors
class ProviderError(ErrorException):
    pass


class WrongResponseException(WarningException):
    def __init__(self, response: HTTPResponse):
        self.response = response


# Info exceptions
