from typing import Any, Callable, Dict, Set, Union
import json
from django.http import HttpResponse
import pytest
from qwant.music.models import Artist
from qwant.music.types import APIData
from qwant.tests import data

GraphQLClient = Callable[..., HttpResponse]
GraphQLResponse = Dict[str, Any]


class TestGraphQLModel:
    @pytest.mark.django_db
    @pytest.mark.parametrize('data', data.API_DATA)
    def test_get_one_artist_basic_info(
        self, data: APIData, graphql_client: GraphQLClient
    ) -> None:
        artist: Artist = Artist.create_from_api_data(**data)
        resp: HttpResponse = graphql_client(
            f'''
            query {{
                artist(slug: "{artist.slug}") {{
                    name
                    slug
                    apiId
                }}
            }}
        ''',
        )
        content: GraphQLResponse = resp.json()['data']
        assert content['artist']['name'] == artist.name
        assert content['artist']['slug'] == artist.slug
        assert content['artist']['apiId'] == artist.api_id

    @pytest.mark.django_db
    def test_get_all_artists(self, graphql_client: GraphQLClient) -> None:
        slugs: Set[str] = set()
        for artist_data in data.API_DATA:
            Artist.create_from_api_data(**artist_data)
            slugs.add(artist_data['slug'])  # type: ignore
            for similar in artist_data['similar_artists']:  # type: ignore
                slugs.add(similar['slug'])  # type: ignore
        resp: HttpResponse = graphql_client(
            '''
        query {
            artists {
                name
                slug
                apiId
            }
        }
        '''
        )
        artists: GraphQLResponse = resp.json()['data']['artists']
        assert {artist['slug'] for artist in artists} == slugs  # type: ignore
