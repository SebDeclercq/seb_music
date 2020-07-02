#!/usr/bin/env python3
'''
Test module for the Artist class handling the Qwant API response.
Author: SebDeclercq (https://www.github.com/SebDeclercq)
'''
from typing import Sequence
import pytest
from qwant.music.models import Artist, SpecialChar
from qwant.music.types import APIData
from qwant.tests import data


@pytest.fixture(autouse=True)
def special_char() -> SpecialChar:
    return SpecialChar.objects.create(orig='ø', dest='o')


class TestArtist:
    @pytest.mark.django_db
    @pytest.mark.parametrize('data', data.API_DATA)
    def test_create_from_api_data(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert artist.name == data['name']
        assert artist.slug == data['slug']
        assert artist.picture == data.get('picture', '')
        assert artist.api_id == data['id']
        assert artist.qwant_url.endswith(data['slug'])

    @pytest.mark.django_db
    @pytest.mark.parametrize('data', data.API_DATA)
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
    @pytest.mark.parametrize('data', data.API_DATA)
    def test_absolute_url(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert (
            artist.get_absolute_url() == f'/qwant/music/artist/id/{artist.pk}'
        )

    @pytest.mark.django_db
    @pytest.mark.parametrize('name, slug', data.NAMES_AND_SLUGS)
    def test_to_slug(self, name: str, slug: str) -> None:
        assert Artist.name_to_slug(name) == slug

    @pytest.mark.real_api_call
    @pytest.mark.django_db
    @pytest.mark.parametrize('name,data', data.NAMES_AND_DATA)
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
    @pytest.mark.parametrize('data', data.API_DATA)
    def test_str_slug(self, data: APIData) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        assert str(artist) == artist.slug

    @pytest.mark.real_api_call
    @pytest.mark.django_db
    @pytest.mark.parametrize('name,api_id', data.NAMES_AND_ID)
    def test_get_one(self, name: str, api_id: int) -> None:
        assert Artist.search_or_add(name).api_id == api_id

    @pytest.mark.django_db
    @pytest.mark.current_dev
    def test_direct_relation(self) -> None:
        orig: Artist = Artist.create_from_api_data(**data.API_DATA[2])
        dest: Artist = Artist.create_from_api_data(**data.API_DATA[3])
        path: Sequence[Artist] = orig.path_to(dest)
        assert path == (orig, dest)

    @pytest.mark.django_db
    @pytest.mark.current_dev
    def test_relation_with_one_node(self) -> None:
        orig: Artist = Artist.create_from_api_data(**data.API_DATA[3])
        middle: Artist = Artist.create_from_api_data(**data.API_DATA[2])
        dest: Artist = Artist.create_from_api_data(**data.API_DATA[4])
        path: Sequence[Artist] = orig.path_to(dest)
        assert path == (orig, middle, dest)

    @pytest.mark.django_db
    @pytest.mark.current_dev
    def test_no_relation(self) -> None:
        orig: Artist = Artist.create_from_api_data(**data.API_DATA[0])
        dest: Artist = Artist.create_from_api_data(**data.API_DATA[4])
        path: Sequence[Artist] = orig.path_to(dest, nb_try=2)
        assert path == ()

    # @pytest.mark.django_db
    # @pytest.mark.current_dev
    # def test_relation_with_two_nodes(self) -> None:
    #     # 6 > 4 > 3 > 5
    #     orig: Artist = Artist.create_from_api_data(**data.API_DATA[5])
    #     middle1: Artist = Artist.create_from_api_data(**data.API_DATA[3])
    #     middle2: Artist = Artist.create_from_api_data(**data.API_DATA[2])
    #     dest: Artist = Artist.create_from_api_data(**data.API_DATA[4])
    #     path: Sequence[Artist] = orig.path_to(dest)
    #     assert path == (orig, middle1, middle2, dest)
