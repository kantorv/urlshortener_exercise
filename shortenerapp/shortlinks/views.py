from django.shortcuts import redirect
from django.http import HttpResponse
import json
from .models import ShortLink
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



@csrf_exempt # POST requests
def create(request):
    """

    example call
    curl -X POST "http://localhost:8034/create" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://ravkavonline.co.il"}'
    """

    if request.method is not "POST":
        return HttpResponse("Method not allowed", status=405)

    try:
        req_body = request.body.decode()  # comes in bytes format, so decoding into string
        data = json.loads(req_body)
        url = data.get('url', None)
    except: # some exception with decoding json data
        return HttpResponse("Invalid data", status=400)

    if url is None:
        return HttpResponse("Invalid URL", status=400)

    link = ShortLink(origin=url)
    link.save()

    shorten_url = link.get_short_url()
    return HttpResponse(shorten_url, status=201)


