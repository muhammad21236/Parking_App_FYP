"""The viewsets for the Rest API endpoints."""
from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import ParkingLot, ParkingLotLog, ParkingLotMonitor, ParkingRequestLog
from .serializers import UserSerializer, GroupSerializer, ParkingLotSerializer, ParkingLotLogSerializer, ParkingLotMonitorSerializer, ParkingRequestLogSerializer

class UserViewSet(ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(ModelViewSet):
    """API endpoint that allows groups to be viewed or edited."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ParkingLotViewSet(ModelViewSet):
    """API endpoint that allows parking lots to be viewed or edited."""
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

class ParkingLotMonitorViewSet(ModelViewSet):
    """API endpoint that allows parking lot monitors to be viewed or edited."""
    queryset = ParkingLotMonitor.objects.all()
    serializer_class = ParkingLotMonitorSerializer

class ParkingLotLogViewSet(ModelViewSet):
    """API endpoint that allows parking lot logs to be viewed or edited."""
    queryset = ParkingLotLog.objects.all()
    serializer_class = ParkingLotLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class ParkingRequestLogViewSet(ModelViewSet):
    """API endpoint that allows parking lot logs to be viewed or edited."""
    queryset = ParkingRequestLog.objects.all()
    serializer_class = ParkingRequestLogSerializer
    permission_classes = [permissions.IsAuthenticated]
