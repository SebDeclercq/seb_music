from typing import Any, Callable, Dict, Union
import json
from django.http import HttpResponse
import pytest
from qwant.music.models import Artist
from qwant.music.types import APIData
from qwant.tests import data


GraphQLResponse = Dict[str, Any]


class TestGraphQLModel:
    @pytest.mark.django_db
    @pytest.mark.parametrize('data', data.API_DATA)
    def test_get_one_artist_basic_info(
        self, data: APIData, graphql_client: Callable[..., HttpResponse]
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
