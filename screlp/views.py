# TODO: split these views into individual files

from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from screlp import forms
from screlp.backend import parse, geog, connect
import time


def home(request):
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
        #form = forms.RegistrationForm(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("It worked!")
        else:
            return HttpResponse("It didn't work! {0}".format(form.errors))
    else:
        request.session["register_error"] = True
        return HttpResponse("It didn't work!") 


def login(request):
    message = "unset"
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            message = "Login worked"
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            message = "user.is_active failed"
    else:
        # Return an 'invalid login' error message.
        message = "user returned None"
    return HttpResponse(message)


def logout(request):
    auth.logout(request)
    return redirect("/")    


def reset_demo_access(request):
    request.session["tries"] = 0
    return redirect("/")


def beta(request):
    c = {}
    logged_in = False
    c.update(csrf(request))
    login = AuthenticationForm()
    register = UserCreationForm()
    #register = forms.RegistrationForm()
    if request.user.is_authenticated():
        logged_in = True

    phrase = "You have 1 try available."
    return render(request, "beta.html", {"logged_in": logged_in,
                                         "demo_available": True,
                                         "login": login,
                                         "csrf": c,
                                         "register": register,
                                         "phrase": phrase})


def result(request):
    args = dict()
    creds = list()
    tracking = list()
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

    creds = settings.YELP_CREDENTIALS  # demo API credentials.
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
