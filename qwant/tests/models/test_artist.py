#!/usr/bin/env python3
'''
Test module for the Artist class handling the Qwant API response.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import List
import pytest
from qwant.music.models import Artist
from qwant.music.types import APIData


API_DATA: List[APIData] = [
    {
        'name': 'Artist-1',
        'slug': 'artist-1',
        'id': 123456,
        'similar_artists': [
            {'name': 'Similar-1', 'slug': 'similar-1', 'id': '789123'},
            {'name': 'Similar-2', 'slug': 'similar-2', 'id': '147258'},
        ],
    },
    {
        'name': 'Artist-2',
        'slug': 'artist-2',
        'id': 456789,
        'similar_artists': [],
    },
]


class TestArtist:
    @pytest.mark.parametrize('data', API_DATA)
    def test_init(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert artist.name == data['name']
        assert artist.slug == data['slug']
        assert artist.api_id == data['id']

    @pytest.mark.django_db
    @pytest.mark.parametrize('data', API_DATA)
    def test_absolute_url(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        artist.save()
        assert (
            artist.get_absolute_url() == f'/qwant/music/artist/id/{artist.pk}'
        )
