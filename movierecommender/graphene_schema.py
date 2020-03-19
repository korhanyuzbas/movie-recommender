import graphene

import movie.schema


class Query(movie.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
