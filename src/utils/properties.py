from logging import Logger
from typing import ClassVar

from .requests import Requests
from ..exceptions import InfoException
from ..types import *
from .html_parser import HtmlParser


class ProviderProperties(object):
    _cache: ClassVar[dict]  # type: dict
    _meta: ClassVar[Meta]  # type: Meta
    _log: ClassVar[Logger]  # type: Logger
    _requests: ClassVar[Requests]  # type: Requests
    _html: ClassVar[HtmlParser]  # type: HtmlParser

    def __init__(self, url: str, **kwargs):
        if 'log' not in kwargs:
            kwargs['log'] = Logger(self.__class__.__name__)
        self._cache = {'url': url}  # type: dict
        self._log = kwargs['log']  # type: Logger

    @property
    def title(self) -> str:
        return self._meta.title

    @property
    def title_original(self) -> str:
        return self._meta.title_original

    @property
    def cover(self) -> str:
        return self._meta.cover

    @property
    def url(self) -> str:
        try:
            return self._meta.url
        except AttributeError:
            return self._cache['url']

    @property
    def content(self):
        if 'content' in self._cache:
            return self._cache.get('content')
        raise InfoException('Content not set yet')

    @content.setter
    def content(self, content):
        self._cache['content'] = content

    @property
    def meta(self) -> Meta:
        return self._meta

    @meta.setter
    def meta(self, meta: Meta):
        if self._meta is not None:
            raise InfoException('Re-init meta')
        self._meta = meta

    @property
    def run_params(self) -> dict:
        return self._cache.get('run_params', {})

    @property
    def request(self) -> Requests:
        return self._requests

    @property
    def html(self) -> HtmlParser:
        if not self._html:
            self._html = HtmlParser()
        return self._html

    # region helpers
    def init_content(self):
        self._cache['content'] = self._requests.get(self.url).read()

    def info(self, message, *args, **kwargs):
        self._log.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._log.warning(message, *args, **kwargs)
        pass
    # endregion helpers

