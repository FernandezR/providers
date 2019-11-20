from typing import Union, List, Dict, Any

from lxml.html import document_fromstring, HtmlElement
from tinycss2 import parser, tokenizer

from ..exceptions import BackgroundImageExtractException, InfoException


class HtmlParser:
    __slots__ = ()
    __dict__: Dict[str, Any] = dict()
    DEFAULT_TRANSLATOR: str = 'html'

    @classmethod
    def select(cls, content: HtmlElement, selector: str) -> List[HtmlElement]:
        return content.cssselect(selector)

    @classmethod
    def select_one(cls, content: HtmlElement, selector: str, idx: int) -> HtmlElement:
        items = cls.select(content, selector)
        return items[idx]

    @classmethod
    def parse(cls, content: str, selector: str = None) -> Union[HtmlElement, List[HtmlElement]]:
        dom = document_fromstring(content)  # type: HtmlElement
        if selector is None:
            return dom
        return cls.select(dom, selector)

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
    def text(cls, element: HtmlElement, strip: bool = True):
        text = element.text.strip() if strip else element.text
        if len(text) < 1:
            raise InfoException('Text has empty')
        return text

    @classmethod
    def text_full(cls, element: HtmlElement, strip: bool = True):
        text = element.text_content().strip() if strip else element.text_content()
        if len(text) < 1:
            raise InfoException('Text has empty')
        return text

    def cover(self, element: HtmlElement, selector: str, attr: str = 'src', idx: int = 0) -> str:
        value = element.cssselect(selector)[idx].get(attr)
        if not value:
            raise RuntimeWarning(self)
        return value
