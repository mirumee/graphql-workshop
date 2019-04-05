from ariadne import gql, make_executable_schema

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
