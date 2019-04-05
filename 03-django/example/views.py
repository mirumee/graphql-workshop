import json
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .graphql import schema


@csrf_exempt
def graphql_view(request):
    if request.method == "GET":
        return HttpResponse(PLAYGROUND_HTML)

    if request.method != "POST":
        return HttpResponseBadRequest()

    if request.content_type != "application/json":
        return HttpResponseBadRequest()

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
