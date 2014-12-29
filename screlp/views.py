from django.shortcuts import render
from django.conf import settings
from screlp.backend import parse, geog, connect
import time


def home(request):
    if "visited" in request.session:
        show_api_fields = False
    else:
        show_api_fields = True
    return render(request, "home.html", {"visited": show_api_fields})


def result(request):
    args = dict()
    creds = list()

    args["address"] = request.GET["a"]
    args["term"] = request.GET["t"]
    args["radius"] = request.GET["r"]
    args["density"] = request.GET["d"]
    args["category"] = request.GET["c"]

    if "visited" in request.session:
        creds = [request.session["con_key"],
                 request.session["con_secret"],
                 request.session["token"],
                 request.session["token_secret"]]
    else:
        creds = settings.YELP_CREDENTIALS

    start = time.time()
    origin = geog.get_geocode(args)
    coords = geog.generate_coords(origin, int(args["density"]), int(args["radius"]))
    yelp_results = parse.scrape_yelp(args, coords, creds)
    """
    if not yelp_results:
        return render(request, "error.html")
    if "visited" not in request.session:
        request.session["visited"] = True
        request.session["con_key"] = request.GET["con_key"]
        request.session["con_secret"] = request.GET["con_secret"]
        request.session["token"] = request.GET["token"]
        request.session["token_secret"] = request.GET["token_secret"]
    """
    time_taken = "Execution time: {:.2f}{}".format((time.time() - start), " seconds")

    orglat, orglong = origin

    return render(request, "result.html", {"args": args,
                                           "coords": coords,
                                           "lat": orglat,
                                           "long": orglong,
                                           "yelp_results": yelp_results,
                                           "exec_time": time_taken})


def clear(request):
    request.session.flush()
    return render(request, "redirect.html")

