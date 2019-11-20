from logging import Logger
from typing import Union

from .html_parser import HtmlParser
from .request import Request
from ..exceptions import InfoException, WarningException
from ..types import *

__all__ = ['ProviderProperties']


class ProviderProperties:
    _cache: dict
    _meta: Meta
    _log: Logger
    _requests: Request
    _html: HtmlParser
    _quiet_mode: bool = False

    def __init__(self, url: str, connection: Request, **kwargs):
        if 'log' not in kwargs:
            kwargs['log'] = Logger(self.__class__.__name__)
        self._cache = {'url': url}  # type: dict
        self._log = kwargs['log']  # type: Logger
        self._requests = connection  # type: Request
        self._quiet_mode = kwargs.get('quiet', False)

    @property
    def title(self) -> str:
        return self._meta.title

    @property
    def title_original(self) -> str:
        return self._meta.title_original

    @property
    def cover(self) -> Union[str, bytes]:
        return self._meta.cover

    @property
    def url(self) -> str:
        try:
            return self._meta.url
        except AttributeError:
            return self._cache['url']

    @property
    def content(self):
        if 'content' not in self._cache:
            raise WarningException('Content not set yet')
        return self._cache.get('content')

    @content.setter
    def content(self, content):
        self._cache['content'] = content

    @property
    def meta(self) -> Meta:
        return self._meta

    @meta.setter
    def meta(self, meta: Meta):
        if self._meta is not None:
            self.info_or_raise('Re-init meta')
        self._meta = meta

    @property
    def run_params(self) -> dict:
        return self._cache.get('run_params', {})

    @property
    def request(self) -> Request:
        return self._requests

    @property
    def html(self) -> HtmlParser:
        if not self._html:
            self._html = HtmlParser()
        return self._html

    @property
    def quiet(self) -> bool:
        return self._quiet_mode

    # region helpers
    def init_content(self):
        self._cache['content'] = self._requests.get(self.url).text

    def info(self, message, *args, **kwargs):
        self._log.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._log.error(message, *args, **kwargs)

    def info_or_raise(self, message, *args, **kwargs):
        if self.quiet:
            self.info_or_raise(message, *args, **kwargs)
        else:
            raise InfoException(message, *args, **kwargs)

    def warning_or_raise(self, message, *args, **kwargs):
        if self.quiet:
            self.warning(message, *args, **kwargs)
        else:
            raise WarningException(message, *args, **kwargs)

    @property
    def chapters_count(self) -> int:
        return self._cache.get('_chapters_count', -1)

    @chapters_count.setter
    def chapters_count(self, count: int):
        self._cache['_chapters_count'] = count

    @property
    def images_count(self) -> int:
        return self._cache.get('_images_count', -1)

    @images_count.setter
    def images_count(self, count: int):
        self._cache['_images_count'] = count

    # endregion helpers

