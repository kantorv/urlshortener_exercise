from django.shortcuts import redirect
from django.http import HttpResponse
import json
from .models import ShortLink
from django.views.decorators.csrf import csrf_exempt
from .utils import validate_url
# Create your views here.



@csrf_exempt # POST requests
def create(request):
    """

    example call
    curl -X POST "http://localhost:8034/create" \
    -H "Content-Type: application/json" \
    -d '{"url": "https://ravkavonline.co.il"}'
    """

    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    try:
        req_body = request.body.decode()  # comes in bytes format, so decoding into string
        data = json.loads(req_body)
        url = data.get('url', None)

    except: # some exception with decoding json data
        return HttpResponse("Invalid data", status=400)

    if url is None:
        return HttpResponse("Invalid URL", status=400)

    #TODO: check why internal validator for url field not works as expected
    #TODO: move this validation to model field validators

    try:
        is_valid = validate_url(url)
        if not is_valid:
            return HttpResponse("Mailformed URL", status=400)
    except:
        return HttpResponse("unknown error", status=500)

    link = ShortLink(origin=url)
    link.save()

    shorten_url = link.get_short_url()
    return HttpResponse(shorten_url, status=201)




def redirect_view(request, hash):
    """
    example call
    curl  "http://localhost:8034/s/asdasds"
    """


    if request.method != "GET":
        return HttpResponse("Method not allowed", status=405)

    try:
        link = ShortLink.objects.get(hash=hash)
        link.increment_clicks() #incrementing clicks
        return redirect(link.origin)
    except ShortLink.DoesNotExist:
        return HttpResponse("link not found", status=404)
    except ShortLink.MultipleObjectsReturned: #should not happen, since hash defined as unique
        return HttpResponse("internal error", status=403)
    except:  #unhandled exeption, for dev team investigation
        #TODO: send exception to sentry/anothe issue tracker
        return HttpResponse("unknown error", status=500)
