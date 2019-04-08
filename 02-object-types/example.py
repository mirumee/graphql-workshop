"""Example 02: Object Types.

Run with::

    $ uvicorn example:app
"""
from ariadne import ObjectType, QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL

# This is our schema
type_defs = gql(
    """
    type Book {
        title: String!
        year: Int!
    }

    type Query {
        books: [Book!]!
    }
"""
)

query = QueryType()  # our Query type


@query.field("books")  # Query.books
def resolve_books(*_):
    return [
        {"title": "The Color of Magic", "year": 1983},
        {"title": "The Light Fantastic", "year": 1986},
        {"title": "Equal Rites", "year": 1987},
    ]


# Create an executable GraphQL schema
schema = make_executable_schema(type_defs, [query])

# Create the ASGI app
app = GraphQL(schema, debug=True)
