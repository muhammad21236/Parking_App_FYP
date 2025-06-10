"""This module contains the views for the Perfect Parking website."""

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import ParkingLot, ParkingLotMonitor
from . import WebPaths
from .utility import record_user_query
import json
from django.conf import settings

def map_view(request):
    return render(request, 'map_template.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })



def home_view(request):  # You can name this whatever makes sense
    # Get all parking lots from database
    parking_lots = ParkingLot.objects.all()

    # Prepare JSON data for the map
    locations = []
    for lot in parking_lots:
        # Handle possible None values for latitude/longitude
        lat = float(lot.latitude) if lot.latitude else 0.0
        lng = float(lot.longitude) if lot.longitude else 0.0

        # Handle vacancy rate (attribute or default)
        try:
            vacancy = float(
                getattr(lot, "vacancy", 0.0)
            )  # Use 'vacancy' attribute or default to 0.0
        except (TypeError, AttributeError):
            vacancy = 0.0

        locations.append(
            {
                "lat": lat,
                "lng": lng,
                "name": lot.name,
                "address": lot.address,
                "id": lot.id,
                "vacancy": vacancy,
                "isPaid": bool(lot.isPaidParking),  # Convert to boolean
            }
        )

    context = {
        "parking_lots": parking_lots,  # For HTML cards
        "locations_json": json.dumps(locations),  # For JavaScript map
    }
    return render(request, "your_template.html", context)


def custom_logout(request):
    """Logs out the user and redirects to the home page."""
    logout(request)
    return redirect("/")


class WebPages:
    HOME_PAGE = "website/index.html"
    PARKING_LOT = "website/parking-lot.html"
    PARKING_LOT_MONITOR = "website/parking-lot-monitor.html"
    PARKING_LOT_MONITORS = "website/parking-lot-monitors.html"
    PARKING_LOTS = "website/parking-lots.html"
    REGISTER_USER = "website/register-user.html"
    LOGIN_USER = "website/login-user.html"
    PRIVACY_POLICY = "website/privacy-policy.html"


# Example view function
def index(request):
    parking_lots = (
        ParkingLot.objects.all()
    )  # Ensure ParkingLot model is imported and queried
    context = {"parking_lots": parking_lots}
    return render(request, "website/index.html", context)


def login_user(request):
    """
    Authenticates and logs in a user based on their submitted username and password.

    Args:
        request: An HttpRequest object that contains metadata about the current request.

    Returns:
        If the submitted form data is valid and the user exists, redirects to the parking lots page. Otherwise,
        redirects to the login page.

    Raises:
        None
    """
    if request.method == "POST":  # FORM SUBMITTED
        username = request.POST["username"]
        password = request.POST["password"]
        tuser = authenticate(request, username=username, password=password)
        if tuser is not None:
            login(request, tuser)
            return redirect(WebPaths.PARKING_LOTS)
        else:
            return redirect(WebPaths.LOGIN)
    else:  # FORM NOT SUBMITTED
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect(WebPages.HOME_PAGE)


def parking_lot(request, parking_lot_id):
    parking_lot = get_object_or_404(ParkingLot, pk=parking_lot_id)
    return render(request, WebPages.PARKING_LOT, {"parking_lot": parking_lot})


def parking_lots(request):
    """Builds the parking lots page.

    Args:
        request (HttpRequest): _description_

    Returns:
        _type_: _description_
    """
    from django.db.models.query import (
        QuerySet,
    )  # Ensure this import is at the top of the file

    parking_lots: QuerySet[ParkingLot] = ParkingLot.objects.all()
    return render(request, WebPages.PARKING_LOTS, {"parking_lots": parking_lots})


def parking_lot_monitor(request, parking_lot_monitor_id):
    parking_lot_monitor = get_object_or_404(
        ParkingLotMonitor, pk=parking_lot_monitor_id
    )
    return render(
        request,
        WebPages.PARKING_LOT_MONITOR,
        {"parking_lot_monitor": parking_lot_monitor},
    )


def parking_lot_monitors(request):  # Search page
    """Builds the parking lot monitors page.

    Args:
        request (HttpRequest): _description_

    Returns:
        _type_: _description_
    """
    from django.db.models.query import (
        QuerySet,
    )  # Ensure this import is at the top of the file

    parking_lot_monitor_list: QuerySet[ParkingLotMonitor] = (
        ParkingLotMonitor.objects.all()
    )

    if request.method == "POST":  # FORM SUBMITTED
        latitude = request.POST["latitude"]
        longitude = request.POST["longitude"]

        record_user_query(latitude, longitude, request)

        context = {
            "parking_lot_monitors": parking_lot_monitor_list,
            "user_point": {"latitude": latitude, "longitude": longitude},
        }
        return render(request, WebPages.PARKING_LOT_MONITORS, context)

    return render(
        request,
        WebPages.PARKING_LOT_MONITORS,
        {"parking_lot_monitors": parking_lot_monitor_list},
    )


def privacy_policy(request):
    """Builds the privacy policy page."""
    return render(request, WebPages.PRIVACY_POLICY)


def register_user(request):
    """Guest User registers to use the app

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            user = form.save()
            # Add first name, last name, and email fields to the user model
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.save()
            return redirect(WebPaths.LOGIN)
    else:
        form = UserCreationForm()
    return render(request, WebPages.REGISTER_USER, {"form": form})

    # load the user details from the request
    # create a new user
