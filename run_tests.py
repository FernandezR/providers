#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from manga_py.providers import get_providers
from manga_py.providers.exceptions import *
from manga_py.providers.types import *
from manga_py.providers.utils.request_utils import *


class TestSummary(unittest.TestCase):

    def test_get_providers_has_data_is_valid(self):
        get_providers('https://readmanga.me/van_pis/')
        self.assertTrue(True)

    def test_get_providers_has_site_not_supported(self):
        with self.assertRaises(ProviderNotFoundError):
            get_providers('https://not-supported/')

    def test_url2name_url_one(self):
        url = 'https://i.imgur.com/sIz74wK_lq.mp4'
        name = url2name(url)
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_url2name_url_two(self):
        url = 'https://i.imgur.com/sIz74wK_lq.mp4/'
        name = url2name(url)
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_url2name_url_three(self):
        url = 'https://i.imgur.com/'
        with self.assertRaises(RuntimeError):
            url2name(url)

    def test_url2name_url_four(self):
        url = 'https://i.imgur.com/sIz74wK_lq.mp4/?abc=&def=123'
        name = url2name(url)
        self.assertEqual('sIz74wK_lq.mp4', name)

    def test_image_one(self):
        url = 'https://i.imgur.com/sIz74wK_lq.mp4'
        image = Image(idx=0, url=url, alternative_urls=[])
        self.assertEqual('000-sIz74wK_lq.mp4', str(image))

    def test_image_two(self):
        url = 'https://i.imgur.com/sIz74wK_lq.mp4'
        image = Image(idx=0, url=url, alternative_urls=[], extension='jpeg', name='video')
        self.assertEqual('000-video.jpeg', str(image))

    def test_image_three(self):
        url = 'https://i.imgur.com/sIz74wK_lq.mp4'
        image = Image(idx=0, url=url, alternative_urls=[], name_format='{extension}/{name}')
        self.assertEqual('mp4/sIz74wK_lq', str(image))


unittest.main()
