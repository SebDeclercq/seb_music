from __future__ import annotations
from typing import Any, Optional
from django.db.models.manager import BaseManager
from graphql.execution.base import ResolveInfo
import graphene
from qwant.music.models import Artist
from .types import ArtistType


class Query(graphene.ObjectType):
    qwant_artist: graphene.Field = graphene.Field(
        ArtistType, slug=graphene.String(), name=graphene.String()
    )
    qwant_artists: graphene.List = graphene.List(
        ArtistType, limit=graphene.Int()
    )

    def resolve_qwant_artist(self, info: ResolveInfo, **kwargs: Any) -> Artist:
        if artist_name := (kwargs.get('slug') or kwargs.get('name')):
            return Artist.search_or_add(artist_name)

    def resolve_qwant_artists(
        self, info: ResolveInfo, limit: Optional[int] = None, **kwargs: Any
    ) -> BaseManager[Artist]:
        return Artist.objects.all()[:limit]
