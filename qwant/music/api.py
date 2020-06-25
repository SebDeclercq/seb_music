#!/usr/bin/env python3
'''
Module for the class collecting data from the unofficial Qwant Music API.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
import requests
from typing import Dict, Final
import json
from qwant.music.types import APIData


class API:
    '''Class directly interacting with the unofficial Qwant Music API.'''

    BASE_URL: Final[str] = 'https://api.qwant.com/music/artist/'

    @classmethod
    def get(cls, slug: str) -> APIData:
        '''Get an artist from the API based on a slug.

        Params:
            slug: The artist's slug to find

        Returns:
            APIData: the parsed JSON response of the API.
        '''
        url: str = cls.BASE_URL + slug
        resp: requests.Response = requests.get(url)
        return resp.json()
