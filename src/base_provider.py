import re
from abc import ABCMeta, abstractmethod
from typing import List, Union, Optional, Iterator

from .exceptions import *
from .types import *
from .utils.properties import ProviderProperties
from .utils.request import Request


class BaseProvider(ProviderProperties, metaclass=ABCMeta):
    DISABLED = False
    AUTO_INIT = True

    def __init__(self, url: str, connection: Request = None, **kwargs):
        url = self._url(url)
        if connection is None:
            connection = Request({})
        super().__init__(url=url, connection=connection)
        kwargs.pop('connection')
        self._cache['run_params'] = kwargs
        self._requests = connection  # type: Request

        if self.AUTO_INIT:
            self.prepare()
            self.meta = self.get_meta()

    @staticmethod
    @abstractmethod
    def supported_urls() -> List[str]:
        """
        Example:
        [
            r'//bato\.to/series/\d',
            r'//www\.mangahere\.cc/manga/\w',
        ]
        """
        raise NotImplementedError()

    @classmethod
    def is_supported(cls, url) -> bool:
        for _url in cls.supported_urls():
            if not cls.DISABLED and re.search(_url, url):
                return True
        return False

    # region abstract
    @staticmethod
    def allow_send_files_referrer() -> bool:
        """ allow send referrer header """
        return True

    @abstractmethod
    def prepare(self):
        self.init_content()
        raise InfoException('Default prepare method')

    @abstractmethod
    def get_chapters(self) -> Iterator[Chapter]:
        raise NotImplementedError()

    @abstractmethod
    def get_chapters_count(self) -> int:
        """ If -1, then continue always """
        return -1

    @abstractmethod
    def get_chapter_files(self, chapter: Chapter) -> Iterator[Union[Image, Archive]]:
        raise NotImplementedError()

    @abstractmethod
    def get_chapter_files_count(self, chapter: Chapter) -> int:
        """ If -1, then continue always """
        return -1

    @abstractmethod
    def get_meta(self) -> Meta:
        raise NotImplementedError()
    # endregion abstract

    # region special methods
    def _url(self, url: str) -> str:
        self.html.items(self.request.get('a').text)
        """ Modify url if need (before init provider) """
        return url

    def _cookies(self, cookies: dict) -> dict:
        """ Modify cookies if need (before init provider) """
        return cookies

    def _headers(self, headers: dict) -> dict:
        """ Modify headers if need (before init provider) """
        return headers

    def flat_chapters(self) -> bool:
        """ This is used when a "chapter" contains maybe only 1 image e.g. pixiv.net """
        return False

    def handle_error(self, state: Exception):
        raise state

    def before_image_save(self, image: Image) -> Optional[LocalImage]:
        """ Manipulate image before saving """
        pass

    def after_image_save(self, image: LocalImage):
        """ Manipulate image after saving """
        pass
    # endregion special methods
