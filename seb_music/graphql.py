import graphene
from qwant.music.graphql.query import Query as QwantMusicQuery


class Query(QwantMusicQuery, graphene.ObjectType):
    pass


schema: graphene.Schema = graphene.Schema(query=Query)