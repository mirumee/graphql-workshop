import json
from ariadne import format_errors, format_error
from ariadne.constants import PLAYGROUND_HTML
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from graphql import graphql_sync


def show_playground(request):
    return HttpResponse(PLAYGROUND_HTML)


def graphql_executor(request, schema):
    # Reject requests that aren't JSON
    if request.content_type != "application/json":
        return HttpResponseBadRequest()

    # Naively read data from JSON request
    try:
        data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest()

    # Check if instance data is not empty and dict
    if not data or not isinstance(data, dict):
        return HttpResponseBadRequest()

    # Check if variables are dict:
    variables = data.get("variables")
    if variables and not isinstance(variables, dict):
        return HttpResponseBadRequest()

    # Execute the query
    result = graphql_sync(
        schema,
        data.get("query"),
        context_value=request,  # expose request as info.context
        variable_values=data.get("variables"),
        operation_name=data.get("operationName"),
    )

    # Build valid GraphQL API response
    status_code = 200
    response = {"data": result.data}
    if result.errors:
        status_code = 400
        response["errors"] = format_errors(result, format_error, debug=settings.DEBUG)

    # Send response to client
    return JsonResponse(response, status=status_code)


@csrf_exempt
def graphql_server(request, schema):
    if request.method == "GET":
        return show_playground(request)
    return graphql_executor(request, schema)
