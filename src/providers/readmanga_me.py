from typing import List, Union, Iterator
import re
import json

from ..base_provider import BaseProvider
from ..types import *
from ..exceptions import ImagesNotFoundException


class ReadMangaMe(BaseProvider):
    @staticmethod
    def supported_urls() -> List[str]:
        return [r'//readmanga\.me/\w']

    def prepare(self):
        self.init_content()
        dom = self.html.items(self.content)
        orig_name = self.html.select(dom, '.names .original-name')
        self.meta = Meta(
            url=self.url,
            author=self.html.text(self.html.select(dom, '.elem_author a.person-link', 0)),
            author_original='',
            title=self.html.text(dom.cssselect('.names .name')[0]),
            title_original='' if len(orig_name) < 1 else self.html.text(orig_name[0]),
            annotation=self.html.text_full(self.html.select(dom, '.manga-description', 0)),
            keywords=[],
            cover=dom.cssselect(),
            rating=9.5,
        )

    def get_chapters(self) -> Iterator[Chapter]:
        items = self.html.items(self.content, '.table tr > td > a')
        self._cache['_chapters_count'] = len(items)
        _re = re.compile(r'/[^/]+/(?:vol)?([^/]+/[^/]+)(?:/|\?ma?t)?')
        for i in items:
            url = i.get('url')
            found = _re.search(url)
            if found is None:
                self.warning("Chapter url has broken: \"{}\"".format(url))
                continue
            substr = found.group(1)
            if ~substr.find('?'):
                substr = substr[:substr.find('?')]
            vol, ch = substr.split('/')
            yield Chapter(
                vol=vol,
                ch=ch,
                url=url,
                name=self.html.text(i),
                # name_format=''
            )

    def get_chapters_count(self) -> int:
        return self._cache['_chapters_count']

    def get_chapter_files(self, chapter: Chapter) -> Iterator[Union[Image, Archive]]:
        content = self.request.get(chapter.url).text
        _re = re.compile(r'rm_h\.init.+?(\[\[.+\]\])')
        images = _re.search(content)

        if images is None:
            raise ImagesNotFoundException(chapter)

        urls = json.loads(images.group(1).replace("'", '"'))  # type: List[list]

        _re_servers = re.search(r'servers\s?=\s?(\[.+\])', content)

        servers: List[str] = []
        if _re_servers is not None:
            _text = _re_servers.group(1).replace("'", '"')
            servers = json.loads(_text) if servers else []

        # ['','https://t7.mangas.rocks/',"auto/33/88/46/One-piece.ru_Credits.png_res.jpg",1250,850]
        for i, u in enumerate(urls):
            yield Image(
                idx=i,
                url='{1}{2}'.format(*u),
                extension='extension',
                alternative_urls=['{}{}'.format(s, u[2]) for s in servers],
                name_format='name_format',
                type='type',
            )

    def get_chapter_files_count(self, chapter: Chapter) -> int:
        return -1

    def get_meta(self) -> Meta:
        pass
