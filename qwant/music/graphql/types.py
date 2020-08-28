from graphene_django.types import DjangoObjectType
from qwant.music.models import Artist


class ArtistType(DjangoObjectType):
    class Meta:
        model: type = Artist
