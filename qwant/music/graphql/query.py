from __future__ import annotations
from typing import Any
from django.db.models import Manager
from graphql.execution.base import ResolveInfo
import graphene
from qwant.music.models import Artist
from .types import ArtistType


class Query(graphene.ObjectType):
    artist: graphene.Field = graphene.Field(ArtistType, slug=graphene.String())
    artists: graphene.List = graphene.List(ArtistType)

    def resolve_artist(self, info: ResolveInfo, **kwargs: Any) -> Artist:
        if slug := kwargs.get('slug'):
            return Artist.objects.get(slug=slug)

    def resolve_artists(
        self, info: ResolveInfo, **kwargs: Any
    ) -> Manager[Artist]:
        return Artist.objects.all()
