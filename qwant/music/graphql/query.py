from __future__ import annotations
from typing import Any, Optional
from django.db.models import Manager
from graphql.execution.base import ResolveInfo
import graphene
from qwant.music.models import Artist
from .types import ArtistType


class Query(graphene.ObjectType):
    artist: graphene.Field = graphene.Field(
        ArtistType, slug=graphene.String(), name=graphene.String()
    )
    artists: graphene.List = graphene.List(ArtistType)

    def resolve_artist(self, info: ResolveInfo, **kwargs: Any) -> Artist:
        if artist_name := (kwargs.get('slug') or kwargs.get('name')):
            return Artist.search_or_add(artist_name)

    def resolve_artists(
        self, info: ResolveInfo, **kwargs: Any
    ) -> Manager[Artist]:
        return Artist.objects.all()
