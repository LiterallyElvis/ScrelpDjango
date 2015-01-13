# TODO: split these views into individual files

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from screlp import forms
from screlp.backend import parse, geog, connect
import time


def home(request):
    logged_in = True
    if not request.user.is_authenticated():
        logged_in = False
    demo_available = True
    login_error = request.GET.get("login_error")
    register_error = request.GET.get("register_error")

    # TODO: Allow users to specify which aspects of the results to receive.

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
                                         "login_error": login_error,
                                         "register_error": register_error,
                                         "demo_available": demo_available,
                                         "phrase": phrase})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        request.session["register_error"] = True
        return redirect("/") 


def login(request):
    username = request.POST.get("user_email", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
    else:
        request.session["login_error"] = True
    return redirect("/")


def reset_demo_access(request):
    request.session["tries"] = 0
    return redirect("/")


def beta(request):
    c = {}
    c.update(csrf(request))
    login = forms.LoginForm()
    register = UserCreationForm()

    phrase = "You have 1 try available."
    return render_to_response("beta.html", RequestContext(request, {"logged_in": False,
                                         "demo_available": True,
                                         "login": login,
                                         "csrf": c,
                                         "register": register,
                                         "phrase": phrase}))


def result(request):
    if "visited" in request.session:
        creds = [request.session["con_key"], request.session["con_secret"],
        request.session["token"], request.session["token_secret"]]
    else:
        creds = settings.YELP_CREDENTIALS  # demo API credentials.
        if "tries" not in request.session.keys():
            request.session["tries"] = 1
        else:
            if request.session["tries"] >= settings.TRIES_ALLOWED:
                return redirect("/")
            request.session["tries"] += 1

    args = dict()
    creds = list()
    tracking = list()

    args["address"] = request.GET.get("a")
    # TODO: handle when address is not passed
    args["term"] = request.GET.get("t")
    args["radius"] = request.GET.get("r", 1)
    args["density"] = max(5, request.GET.get("d", 1))
    args["category"] = request.GET.get("c")
    radius = int(args["radius"]) * 1609.34  # convert to meters


    start = time.time()
    origin = geog.get_geocode(args)
    coords = geog.generate_coords(origin, int(args["density"]), int(args["radius"]))
    yelp_results = parse.scrape_yelp(args, coords, creds)
    time_taken = "Execution time: {:.2f} {}".format((time.time() - start), "seconds")

    orglat, orglong = origin

    return render(request, "result.html", {"args": args,
                                           "coords": coords,
                                           "lat": orglat,
                                           "long": orglong,
                                           "radius": radius,
                                           "yelp_results": yelp_results,
                                           "exec_time": time_taken})
