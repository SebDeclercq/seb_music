#!/usr/bin/env python3
'''
Test module for the Artist class handling the Qwant API response.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import List, Sequence, Tuple
import pytest
from qwant.music.models import Artist, SpecialChar
from qwant.music.types import APIData


API_DATA: List[APIData] = [
    {
        'name': 'Artist-1',
        'slug': 'artist-1',
        'id': 123456,
        'similar_artists': [
            {'name': 'Similar-1', 'slug': 'similar-1', 'id': 789123},
            {'name': 'Similar-2', 'slug': 'similar-2', 'id': 147258},
        ],
        'picture': 'http://www.example.org/pic1',
    },
    {
        'name': 'Artist-2',
        'slug': 'artist-2',
        'id': 456789,
        'similar_artists': [],
    },
]


names_and_slugs: Sequence[Tuple[str, str]] = (
    ('hello', 'hello'),
    ('Hello', 'hello'),
    ('Hello World', 'hello-world'),
    ('Tiësto', 'tiesto'),
    ('Satin- -Jackets', 'satin-jackets'),
    ('==hel++lo==', 'hello'),
    ('Blank & Jones', 'blank-jones'),
    ('Møme', 'mome'),
)


names_and_data: Sequence[Tuple[str, APIData]] = (
    (
        'Goldroom',
        {
            'slug': 'goldroom',
            'id': 260920179,
            'similar_artist_name': 'Satin Jackets',
        },
    ),
    (
        'Satin Jackets',
        {
            'slug': 'satin-jackets',
            'id': 441748199,
            'similar_artist_name': 'Goldroom',
        },
    ),
)

names_and_id: Sequence[Tuple[str, int]] = (
    ('Goldroom', 260920179),
    ('Satin Jackets', 441748199),
)


@pytest.fixture(autouse=True)
def special_char() -> SpecialChar:
    return SpecialChar.objects.create(orig='ø', dest='o')


class TestArtist:
    @pytest.mark.django_db
    @pytest.mark.parametrize('data', API_DATA)
    def test_create_from_api_data(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert artist.name == data['name']
        assert artist.slug == data['slug']
        assert artist.picture == data.get('picture', '')
        assert artist.api_id == data['id']
        assert artist.qwant_url.endswith(data['slug'])

    @pytest.mark.django_db
    @pytest.mark.parametrize('data', API_DATA)
    def test_similar_artists(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        for similar_artist in artist.similar_artists.all():
            assert isinstance(similar_artist, Artist)
            assert similar_artist.name in [
                sim['name'] for sim in data['similar_artists']
            ]
            assert similar_artist.api_id in [
                sim['id'] for sim in data['similar_artists']
            ]

    @pytest.mark.django_db
    @pytest.mark.parametrize('data', API_DATA)
    def test_absolute_url(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert (
            artist.get_absolute_url() == f'/qwant/music/artist/id/{artist.pk}'
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, slug', names_and_slugs)
    def test_to_slug(self, name: str, slug: str) -> None:
        assert Artist.name_to_slug(name) == slug

    @pytest.mark.real_api_call
    @pytest.mark.django_db
    @pytest.mark.parametrize('name,data', names_and_data)
    def test_create_from_api(self, name: str, data: APIData) -> None:
        artist: Artist = Artist.create_from_api(name)
        assert artist.name == name
        assert artist.slug == data['slug']
        assert artist.api_id == data['id']
        assert data['similar_artist_name'] in [
            sim.name for sim in artist.similar_artists.all()
        ]
        if artist.picture:
            assert artist.picture.startswith('http')

    @pytest.mark.django_db
    @pytest.mark.parametrize('data', API_DATA)
    def test_str_slug(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert str(artist) == artist.slug

    @pytest.mark.real_api_call
    @pytest.mark.django_db
    @pytest.mark.parametrize('name,api_id', names_and_id)
    def test_get_one(self, name: str, api_id: int) -> None:
        assert Artist.search_or_add(name).api_id == api_id
