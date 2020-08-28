import graphene
from .query import Query

schema: graphene.Schema = graphene.Schema(query=Query)
