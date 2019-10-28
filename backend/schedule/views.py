from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
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

@api_view(['GET', 'DELETE'])
def slotDetail(request, StartDate, EndDate):
    try:
        slot = Slot.objects.get(start_time=startDate)
    except Slot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SlotSerializer(slot, context={'request': request})
        return Response(serializer.data)
