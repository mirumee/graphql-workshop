"""Example 01: The Basics.

Run with::

    $ uvicorn example:app
"""
from ariadne import MutationType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

# This is our schema
type_defs = gql(
    """
    type Query {
        hello: String!
    }

    type Mutation {
        add(a: Int!, b: Int!): Int!
    }
"""
)

query = QueryType()  # our Query type
mutation = MutationType()  # our Mutation type


@query.field("hello")  # Query.hello
def resolve_hello(*_):
    return "Hello DjangoCon!"


@mutation.field("add")  # Mutation.add
def resolve_add(*_, a: int, b: int):
    return a + b


# Create an executable GraphQL schema
schema = make_executable_schema(type_defs, [query, mutation])

# Create the ASGI app
app = GraphQL(schema, debug=True)
