from typing import ClassVar, Union, Tuple, Dict
from pathlib import Path

from urllib.parse import urlparse
from requests import Session, Response
from requests.cookies import cookiejar_from_dict, RequestsCookieJar
from requests.adapters import HTTPAdapter
from ..exceptions import *
from cloudscraper import CloudScraper


__all__ = ['Request']


class Request:
    _headers: ClassVar[dict] = dict()
    _session: ClassVar[Session]

    def __init__(self, headers: dict):
        self._headers.update(headers or {})
        default_adapter = HTTPAdapter(max_retries=3)
        self._session = Session()
        self._session.adapters = [default_adapter]

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, session: Session):
        self._session = session

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, headers: dict):
        self.headers = headers

    def headers_update(self, headers: dict):
        self.headers.update(headers)

    @property
    def cookies(self) -> RequestsCookieJar:
        return self._session.cookies

    @cookies.setter
    def cookies(self, cookies: dict):
        self._session.cookies = cookiejar_from_dict(cookies)

    def cookies_update(self, cookies: dict):
        self._session.cookies.update(cookies)

    def request(self, method, url, has_referer: bool = True, **kwargs) -> Response:
        kwargs.setdefault('headers', {})
        kwargs['headers'].update(self._headers)
        if not has_referer and kwargs.get('headers', {}).get('Referer') is not None:
            del kwargs['headers']['Referer']
        return self._session.request(method=method, url=url, **kwargs)

    def get(self, url: str, **kwargs) -> Response:
        kwargs.setdefault('allow_redirects', True)
        return self.request(method='GET', url=url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self.request(method='POST', url=url, **kwargs)

    @classmethod
    def url2name(cls, url: str) -> str:
        path = urlparse(url).path
        return path[path.find('/') + 1:]

    def download(self, url: str, path: Path, name: Union[str, Path]):
        """ path """
        response = self.get(url)
        _path = str(path.resolve().joinpath(name or self.url2name(response.url)))
        with open(_path, 'wb') as w:
            if not w.writable():
                raise CantWriteFileException(_path)
            w.write(response.content)

    def cf_scrape(self, url: str, **kwargs):
        if 'User-Agent' in self.headers:
            kwargs.setdefault('browser', self.headers['User-Agent'])
        tokens = CloudScraper.get_tokens(url, **kwargs)  # type: Tuple[dict, str]
        self.cookies_update(tokens[0])
        # self.headers.update({'User-Agent': tokens[1]})
        return tokens[1]
