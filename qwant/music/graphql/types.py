from django.urls import reverse
from graphene_django.types import DjangoObjectType
from graphql.execution.base import ResolveInfo
import graphene
from qwant.music.models import Artist


class ArtistType(DjangoObjectType):
    url: graphene.String = graphene.String()
    qwant_url: graphene.String = graphene.String()

    class Meta:
        model: type = Artist

    def resolve_url(self, info: ResolveInfo) -> str:
        return reverse('qwant:artist_detail', kwargs={'pk': self.pk})

    def resolve_qwant_url(self, info: ResolveInfo) -> str:
        return self.qwant_url

