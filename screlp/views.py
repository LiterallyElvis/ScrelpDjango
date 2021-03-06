# TODO: split these views into individual files

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.context_processors import csrf
from screlp.backend import parse, geog, connect
from screlp import models, forms


def home(request):
    logged_in = False
    demo_available = True
    login_error = request.GET.get("login_error")
    register_error = request.GET.get("register_error")

    c = {}
    c.update(csrf(request))
    login = AuthenticationForm()
    register = UserCreationForm()

    # TODO: Allow users to specify which results to receive.

    if "tries" not in request.session.keys():
        request.session["tries"] = 0

    if request.session["tries"] >= settings.TRIES_ALLOWED:
        demo_available = False
    if request.user.is_authenticated():
        logged_in = True

    number_of = max(0, settings.TRIES_ALLOWED - int(request.session["tries"]))
    tries = "tries"
    if number_of == 1:
        tries = "try"
    phrase = "You have {0} {1} available.".format(number_of, tries)
    return render(request, "home.html", {"logged_in": logged_in,
                                         "csrf": c,
                                         "login": login,
                                         "register": register,
                                         "login_error": login_error,
                                         "register_error": register_error,
                                         "demo_available": demo_available,
                                         "phrase": phrase})


def beta(request):
    c = {}
    c.update(csrf(request))
    login = forms.LoginForm()
    register = forms.RegistrationForm()

    phrase = "You have 1 try available."
    return render(request, "beta.html", {"logged_in": False,
                                         "csrf": c,
                                         "login": login,
                                         "register": register,
                                         "demo_available": True,
                                         "phrase": phrase})


def autocomplete(request):
    from screlp.models import Categories
    import json

    query = request.GET.get("term")
    query_results = Categories.objects.all().filter(yelp_name__startswith=query)
    results = []
    for result in query_results:
        category = {}
        category["id"] = result.id
        category["label"] = result.human_name
        category["value"] = result.yelp_name
        results.append(category)
    data = json.dumps(results)

    return HttpResponse(data, "application/json")


def login(request):
    message = "unset"
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return redirect("/")
        else:
            # TODO: Return a 'disabled account' error message
            return HttpResponse("user.is_active failed")
    else:
        # TODO: Return an 'invalid login' error message.
        return HttpResponse("user returned None")


def logout(request):
    auth.logout(request)
    return redirect("/")


def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        #form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(request.POST["password"])
            new_user.save()
            #new_user = auth.authenticate(username=username, password=password)
            #auth.login(request, new_user)
            return redirect("/")
        else:
            return HttpResponse("It didn't work!\n{0}".format(form.errors))
    else:
        request.session["register_error"] = True
        return HttpResponse("It didn't work!")


def settings_page(request):
    form = forms.UpdateApiKeyForm()
    return render(request, "settings.html", {"api_update": form})


def reset_demo_access(request):
    request.session["tries"] = 0
    return redirect("/")


def result(request):
    args = dict()
    creds = list()

    if False: # TODO: user authentication check
        creds = [request.session["con_key"], request.session["con_secret"],
        request.session["token"], request.session["token_secret"]]
    else:
        creds = settings.YELP_CREDENTIALS  # demo API credentials.
        if "tries" not in request.session.keys():
            request.session["tries"] = 1
        else:
            if request.session["tries"] >= settings.TRIES_ALLOWED and not request.user.is_authenticated():
                return redirect("/")
            else:
                request.session["tries"] += 1

    args["address"] = request.GET.get("a")
    # TODO: handle when address is not passed
    args["term"] = request.GET.get("t")
    args["radius"] = request.GET.get("r", 1)
    args["density"] = max(5, request.GET.get("d", 1))
    args["category"] = request.GET.get("c")
    radius = int(args["radius"]) * 1609.34  # convert to meters

    origin = geog.get_geocode(args)
    coords = geog.generate_coords(origin, int(args["density"]), int(args["radius"]))
    yelp_results = parse.scrape_yelp(args, coords, creds)
    orglat, orglong = origin

    return render(request, "result.html", {"args": args,
                                           "coords": coords,
                                           "lat": orglat,
                                           "long": orglong,
                                           "radius": radius,
                                           "yelp_results": yelp_results})
