"""This file is used to register the models in the admin page."""

from django.contrib import admin
from PerfectParking.models import ParkingLot, ParkingLotMonitor, ParkingRequestLog, ParkingLotLog

# Register your models here.

admin.site.register(ParkingLot)
admin.site.register(ParkingLotMonitor)
admin.site.register(ParkingLotLog)
admin.site.register(ParkingRequestLog)
