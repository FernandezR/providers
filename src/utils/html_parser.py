from typing import Union, List

from lxml.html import document_fromstring, HtmlElement
from tinycss2 import parser
from urllib3.response import HTTPResponse


class HtmlParser:
    @classmethod
    def from_string(cls, content: str, selector: str = None, idx: int = None) -> Union[HtmlElement, List[HtmlElement]]:
        dom = document_fromstring(content)  # type: HtmlElement
        if selector is not None:
            dom = dom.cssselect(selector)
        if idx is not None:
            dom = dom[idx]
        return dom

    @classmethod
    def from_response(cls, response: HTTPResponse) -> HtmlElement:
        return cls.from_string(response.read())

    @classmethod
    def background_image(cls, element: HtmlElement):
        return  # todo

    @classmethod
    def extract_attribute(cls, items: Union[list, tuple], attribute: str = None):
        return [i.get(attribute) for i in items]
