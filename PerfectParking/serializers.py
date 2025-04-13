"""Serializers for the PerfectParking app."""
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ParkingLot, ParkingLotLog, ParkingLotMonitor, ParkingRequestLog

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    A serializer for the User model."""
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """ this is a serializer for the Group model"""
    class Meta:
        model = Group
        fields = ['url', 'name']
        
class ParkingLotSerializer(serializers.HyperlinkedModelSerializer):
    """ this is a serializer for the ParkingLot model"""
    class Meta:
        model = ParkingLot
        fields = ['id', 'name', 'latitude', 'longitude']

class ParkingLotMonitorSerializer(serializers.HyperlinkedModelSerializer):
    """this is a serializer for the ParkingLotMonitor model"""
    class Meta:
        """this is a serializer for the ParkingLotMonitor model
        """
        model = ParkingLotMonitor
        fields = ['id', 'name', 'latitude', 'longitude', 'probabilityParkingAvailable', 'free_parking_spaces']

class ParkingLotLogSerializer(serializers.HyperlinkedModelSerializer):
    """this is a serializer for the ParkingLotLog model"""
    class Meta:
        """this is a serializer for the ParkingLotLog model"""
        model = ParkingLotLog
        fields = [ 'url','id', 'parking_lot', 'logged_by_monitor', 'free_parking_spaces', 'time_stamp' ]

class ParkingRequestLogSerializer(serializers.HyperlinkedModelSerializer):
    """this is a serializer for the ParkingRequestLog model"""
    class Meta:
        """this is a serializer for the ParkingRequestLog model"""
        model = ParkingRequestLog
        fields = [ 'url','id', 'area_of_interest_latitude', 'area_of_interest_longitude', 'time_stamp', 'user', 'user_ip_address' ]
