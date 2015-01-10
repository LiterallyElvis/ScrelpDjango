# TODO: split these views into individual files

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect
from screlp.backend import parse, geog, connect
import time


def home(request):
    logged_in = False
    demo_available = True

    if "tries" not in request.session.keys():
        request.session["tries"] = 0

    if request.session["tries"] >= settings.TRIES_ALLOWED:
        demo_available = False
    if request.user.is_authenticated():
        logged_in = True

    tries = max(0, settings.TRIES_ALLOWED - int(request.session["tries"]))
    term = "tries"
    if tries == 1:
        term = "try"
    phrase = "You have {0} {1} available.".format(tries, term)
    return render(request, "home.html", {"logged_in": logged_in,
                                         "demo_available": demo_available,
                                         "phrase": phrase})


def reset_demo_access(request):
    del request.session["tries"]
    return redirect('/')


def result(request):
    args = dict()
    creds = list()
    tracking = list()

    args["address"] = request.GET.get("a")
    # TODO: handle when address is not passed
    args["term"] = request.GET.get("t")
    args["radius"] = request.GET.get("r", 1)
    args["density"] = request.GET.get("d", 1)
    args["category"] = request.GET.get("c")
    radius = int(args["radius"]) * 1609.34  # convert to meters

    # TODO: Allow users to specify which aspects of the results to receive.

    if "visited" in request.session:
        creds = [request.session["con_key"], request.session["con_secret"],
                 request.session["token"], request.session["token_secret"]]
    else:
        creds = settings.YELP_CREDENTIALS  # demo API credentials.
        if "tries" not in request.session.keys():
            request.session["tries"] = 1
        else:
            request.session["tries"] += 1

    start = time.time()
    origin = geog.get_geocode(args)
    coords = geog.generate_coords(origin, int(args["density"]), int(args["radius"]))
    yelp_results = parse.scrape_yelp(args, coords, creds)
    time_taken = "Execution time: {:.2f}{}".format((time.time() - start), " seconds")

    orglat, orglong = origin

    return render(request, "result.html", {"args": args,
                                           "coords": coords,
                                           "lat": orglat,
                                           "long": orglong,
                                           "radius": radius,
                                           "yelp_results": yelp_results,
                                           "exec_time": time_taken})
