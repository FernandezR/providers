#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from manga_py.providers import get_providers
from manga_py.providers.exceptions import *
from manga_py.providers.types import *
from manga_py.providers.utils.request_utils import *
from manga_py.providers.utils.html_parser import HtmlParser
from lxml.html import HtmlElement


class TestSummary(unittest.TestCase):
    default_manga_url = 'https://readmanga.me/van_pis/'
    default_chapter_url = 'https://readmanga.me/van_pis/0/1.5'
    default_image_url = 'https://i.imgur.com/sIz74wK_lq.mp4'
    default_html = '<html><title>Title</title><body>' \
                   '<a href="{ch}">Link text</a>' \
                   '<div class="image" style="background: url({img})"><img src="{img}"<div>' \
                   '<div class="bad-image" style="background: url()"></div>' \
                   '<div class="inner-element-text"><span>text</text></div>' \
                   '<div class="empty-element" title="element-title"></div>' \
                   '<div class="space-only-element"> </div>' \
                   '</body></html>'.format(ch=default_chapter_url, img=default_image_url)

    def test_get_providers_has_data_is_valid(self):
        get_providers(self.default_manga_url)
        self.assertTrue(True)

    def test_get_providers_has_site_not_supported(self):
        with self.assertRaises(ProviderNotFoundError):
            get_providers('https://not-supported/')

    def test_url2name_url_one(self):
        name = url2name(self.default_image_url)
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_url2name_url_two(self):
        name = url2name(self.default_image_url + '/')
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_url2name_url_three(self):
        url = 'https://i.imgur.com/'
        with self.assertRaises(RuntimeError):
            url2name(url)

    def test_url2name_url_four(self):
        url = self.default_image_url + '/?abc=&def=123'
        name = url2name(url)
        self.assertEqual('sIz74wK_lq.mp4', name)

    @classmethod
    def _image(cls, **kwargs):
        kwargs.setdefault('idx', 0)
        kwargs.setdefault('url', cls.default_image_url)
        kwargs.setdefault('alternative_urls', [])
        return Image(**kwargs)

    @classmethod
    def _chapter(cls, **kwargs):
        kwargs.setdefault('vol', '0')
        kwargs.setdefault('ch', '1')
        kwargs.setdefault('name', 'name')
        kwargs.setdefault('url', cls.default_chapter_url)
        return Chapter(**kwargs)

    def test_image_one(self):
        self.assertEqual('000-sIz74wK_lq.mp4', str(self._image()))

    def test_image_two(self):
        self.assertEqual('000-video.jpeg', str(self._image(extension='jpeg', name='video')))

    def test_image_three(self):
        self.assertEqual('mp4/sIz74wK_lq', str(self._image(name_format='{extension}/{name}')))

    def test_image_without_extension(self):
        url = self.default_image_url[:self.default_image_url.rfind('.')]
        self.assertEqual('000-sIz74wK_lq.png', str(self._image(url=url)))

    def test_chapter_default(self):
        self.assertEqual('vol_000_ch_001-name', str(self._chapter()))

    def test_chapter_name_format(self):
        self.assertEqual('awesome-000_ch_001', str(self._chapter(name_format='awesome-{vol:>03}_ch_{ch:>03}')))

    def test_parser(self):
        html = HtmlParser.parse(self.default_html)
        self.assertEqual(len(HtmlParser.parse(self.default_html, 'a')), 1)
        title = HtmlParser.select_one(html, 'title', 0)
        self.assertEqual(HtmlParser.text(title), 'Title')
        self.assertIsInstance(html, HtmlElement)

    def test_background_image(self):
        html = HtmlParser.parse(self.default_html)
        self.assertEqual(
            self.default_image_url,
            HtmlParser.background_image(HtmlParser.select_one(html, 'div.image', 0))
        )
        with self.assertRaises(BackgroundImageExtractException) as e:
            HtmlParser.background_image(HtmlParser.select_one(html, 'div.bad-image', 0))
        self.assertEqual('background: url()', e.exception.style)

    def test_get_empty_text(self):
        html = HtmlParser.parse(self.default_html)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text(HtmlParser.select_one(html, 'div.empty-element', 0))
        self.assertEqual(('Element not have text',), e.exception.args)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text(HtmlParser.select_one(html, 'div.inner-element-text', 0))
        self.assertEqual(('Element not have text',), e.exception.args)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text(HtmlParser.select_one(html, 'div.space-only-element', 0))
        self.assertEqual(('Text is too short',), e.exception.args)

        with self.assertRaises(InfoException) as e:
            HtmlParser.text_full(HtmlParser.select_one(html, 'div.space-only-element', 0))
        self.assertEqual(('Text is too short',), e.exception.args)

        self.assertEqual('text', HtmlParser.text_full(HtmlParser.select_one(html, 'div.inner-element-text', 0)))

    def test_attributes(self):
        elements = HtmlParser.parse(self.default_html, '.empty-element')
        self.assertEqual(['element-title'], HtmlParser.extract_attribute(elements, 'title'))

    def test_cover(self):
        html = HtmlParser.parse(self.default_html)
        self.assertEqual(self.default_image_url, HtmlParser.cover(html, '.image > img'))


unittest.main()
