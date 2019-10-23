from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, ReservationSerializer, FileSerializer, SlotSerializer
from .models import User, Reservation, File, Slot


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ReservationView(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

class FileView(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

class SlotView(viewsets.ModelViewSet):
    serializer_class = SlotSerializer
    queryset = Slot.objects.all()
