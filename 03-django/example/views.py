import json
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .graphql import schema


def show_playground(request):
    return HttpResponse(PLAYGROUND_HTML)


def graphql_executor(request):
    # Reject requests that aren't JSON
    if request.content_type != "application/json":
        return HttpResponseBadRequest()

    # Naively read data from JSON request
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest()

    # Execute the query
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,  # expose request as info.context
        debug=settings.DEBUG,
    )

    status_code = 200 if success else 400
    # Send response to client
    return JsonResponse(result, status=status_code)


@csrf_exempt
def graphql_view(request):
    if request.method == "GET":
        return show_playground(request)
    return graphql_executor(request)
