"""Example 01: The Basics.

Run with::

    $ uvicorn example:app
"""
from ariadne import gql, make_executable_schema
from ariadne.asgi import GraphQL

# This is our schema
type_defs = gql(
    """
    type Query {
        hello: String!
    }
"""
)

# Create an executable GraphQL schema
schema = make_executable_schema(type_defs, [])

# Create the ASGI app
app = GraphQL(schema)
