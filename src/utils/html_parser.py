from typing import Union, List

from lxml.html import document_fromstring, HtmlElement
from requests import Response
from tinycss2 import parser, tokenizer

from ..exceptions import BackgroundImageExtractException


class HtmlParser:
    @classmethod
    def items(cls, content: str, selector: str = None, idx: int = None) -> Union[HtmlElement, List[HtmlElement]]:
        dom = document_fromstring(content)  # type: HtmlElement
        if selector is not None:
            dom = dom.cssselect(selector)  # type: List[HtmlElement]
        if idx is not None:
            dom = dom[idx]
        return dom

    @classmethod
    def background_image(cls, element: HtmlElement) -> str:
        style = element.get('style')
        url = [i for i in parser.parse_component_value_list(style) if isinstance(i, tokenizer.URLToken)]
        if len(url) < 1:
            raise BackgroundImageExtractException(style)
        return url[-1].value

    @classmethod
    def extract_attribute(cls, items: List[HtmlElement], attribute: str = None, strip: bool = True) -> List[str]:
        return [(i.get(attribute).strip() if strip else i.get(attribute)) for i in items]

    @classmethod
    def elements(cls, data: Union[str, Response], selector: str):
        if isinstance(data, Response):
            data.raise_for_status()
            data = data.text
        return cls.items(data, selector)
