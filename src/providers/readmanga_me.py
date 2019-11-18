from typing import List, Union, Iterator

from ..base_provider import BaseProvider
from ..types import *


class ReadMangaMe(BaseProvider):
    @staticmethod
    def supported_urls() -> List[str]:
        return [r'//readmanga\.me/\w']

    def prepare(self):
        self.init_content()

    def get_chapters(self) -> Iterator[Chapter]:
        items = self.html.from_string(self.content, '.table tr > td > a')
        return self.html.extract_attribute(items)

    def get_chapters_count(self) -> int:
        return -1

    def get_chapter_files(self, chapter: Chapter) -> Iterator[Union[Image, Archive]]:
        pass

    def get_chapter_files_count(self, chapter: Chapter) -> int:
        return -1

    def get_meta(self) -> Meta:
        pass
