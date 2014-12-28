"""
geog.py is a component of Screlp that manages anything related to geography.

The first function is get_geocode, which uses the pygeocoder module to retrieve
GPS coordinates when supplied with a verbose address.

The next function, haversine, is taken from a very helpful man named Wayne Dyck
who posted the haversine formula online. It has been modified to use miles
instead of kilometers.

The last function is the true magic of screlp, a grid coordinate generator.
Not a python generator, but rather a function that generates a grid of
coordinates based on a single input coordinateself.
"""

from pygeocoder import Geocoder
import math

X_INCREMENT = .014474  # approximately one latitude mile in decimal degrees
Y_INCREMENT = .016761  # approximately one lonitude mile in decimal degrees
METERS_PER_MILE = 1609  # number of meters in a mile.
EARTH_RADIUS_IN_MILES = 3959  # radius of earth, in miles


def get_geocode(args):
    """
    Returns GPS coordinates from Google Maps for a given location.
    """
    result = Geocoder.geocode(args['address'])
    lat, lon = result[0].coordinates
    lat = round(lat, 6)
    lon = round(lon, 6)
    return lat, lon


def haversine(origin, destination):
    """
    Author: Wayne Dyck
    http://www.platoscave.net/blog/2009/oct/5/
                 calculate-distance-latitude-lonitude-python/
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    delta_lat = math.radians(lat2-lat1)
    delta_lon = math.radians(lon2-lon1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) \
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) \
        * math.sin(delta_lon/2) * math.sin(delta_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = round(EARTH_RADIUS_IN_MILES * c, 2)

    return distance


def generate_coords(origin, density=1, radius=1, radius_enforced=True):
    """
    Returns list of coordinates, given a single origin coordinate (expressed in
    decimal degrees), a radius (expressed in miles), and a density value.
    """
    coords = []
    limit = int(math.sqrt(((2 * density) + 1)**2))  # y = (2x+1)
    a, b = origin
    lat_mod = X_INCREMENT * radius
    lon_mod = Y_INCREMENT * radius
    lat_max = a + lat_mod
    lon_min = b - lon_mod
    lat_min = a - lat_mod
    lon_max = b + lon_mod
    a, b = lat_max, lon_min
    for x in range(0, limit):
        for y in range(0, limit):
            lat = float("%.6f" % (a - (x * (lat_mod / density))))
            lon = float("%.6f" % (b + (y * (lon_mod / density))))
            new_coord = (lat, lon)
            if radius_enforced:
                if haversine(new_coord, origin) > radius:
                    pass
                else:
                    if new_coord not in coords:
                        coords.append(new_coord)
            else:
                if new_coord not in coords:
                    coords.append(new_coord)

    return coords
