from ariadne.asgi import GraphQL
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from .graphql import schema


graphql_server = GraphQL(schema, debug=True)

application = ProtocolTypeRouter({
    'http': URLRouter([
        path("graphql/", graphql_server),
        path("", AsgiHandler)
    ]),
    'websocket': URLRouter([
        path("graphql/", graphql_server),
    ])
})
