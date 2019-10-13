from django.shortcuts import render
from rest_framework import viewsets
from .serializers import StudentSerializer, ReservationSerializer, FileSerializer, SlotSerializer
from .models import Student, Reservation, File, Slot


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class ReservationView(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

class FileView(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    queryset = File.objects.all()

class SlotView(viewsets.ModelViewSet):
    serializer_class = SlotSerializer
    queryset = Slot.objects.all()
