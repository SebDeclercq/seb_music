from typing import Any
from graphql.execution.base import ResolveInfo
import graphene
from qwant.music.models import Artist
from .types import ArtistType


class Query(graphene.ObjectType):
    artist: graphene.Field = graphene.Field(ArtistType, slug=graphene.String())

    def resolve_artist(self, info: ResolveInfo, **kwargs: Any) -> Artist:
        if slug := kwargs.get('slug'):
            return Artist.objects.get(slug=slug)
