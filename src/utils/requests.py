from typing import ClassVar
from urllib3 import HTTPConnectionPool
from urllib3 import HTTPResponse


class Requests(object):
    _connection: ClassVar[HTTPConnectionPool]  # type: HTTPConnectionPool

    def __init__(self, connection: HTTPConnectionPool):
        self._connection = connection

    def get(self, url, **kwargs) -> HTTPResponse:
        return self._connection.request('GET', url=url, **kwargs)

    def post(self, url, **kwargs) -> HTTPResponse:
        return self._connection.request('POST', url=url, **kwargs)

    @property
    def connection(self) -> HTTPConnectionPool:
        return self._connection
