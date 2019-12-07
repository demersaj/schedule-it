# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

#Added for APIView classes.
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from schedule.models import ScheduleUser, Reservation, File, Slot
from schedule.serializers import ScheduleUserSerializer, ReservationSerializer, FileSerializer, SlotSerializer, CreateSlotSerializer, CreateReservationSerializer

################################################################################
################################################################################
# All functions for retrieving users.
################################################################################
################################################################################
class ScheduleUserList(APIView):
    """
    List all scheduleusers.
    """
    queryset = ScheduleUser.objects.none()
    def get(self, request, format=None):
        users = ScheduleUser.objects.all()
        serializer = ScheduleUserSerializer(users , many=True)
        return Response(serializer.data)

class ScheduleUserDetail(APIView):
    """
    Retrieve a scheduleuser instance by id.
    """
    queryset = ScheduleUser.objects.none()
    def get(self, request, pk, format=None):
        suser = ScheduleUser.objects.filter(id=pk)
        if(len(suser) == 0):
            raise Http404
        serializer = ScheduleUserSerializer(suser, many=True)
        return Response(serializer.data)

class ScheduleUserDetailByOnid(APIView):
    """
    Retrieve a user instance by ONID.
    """
    queryset = ScheduleUser.objects.none()
    def get(self, request, onid, format=None):
        suser = ScheduleUser.objects.filter(onid=onid)
        if(len(suser) == 0):
            raise Http404
        serializer = ScheduleUserSerializer(suser, many=True)
        return Response(serializer.data)

class ScheduleUsersRegisteredForASlot(APIView):
    """
    List all users registered for a slot.
    """
    queryset = ScheduleUser.objects.none()
    def get(self, request, slot_id, format=None):
        reservations = Reservation.objects.filter(slot=slot_id)
        users = ScheduleUser.objects.none()
        for r in reservations:
            users |= ScheduleUser.objects.filter(id = r.owner.id)
        serializer = ScheduleUserSerializer(users , many=True)
        return Response(serializer.data)

################################################################################
################################################################################
# All functions for retrieving, creating, updating, and deleting slots.
################################################################################
################################################################################
class SlotList(APIView):
    """
    List all slots, or create a new slot.
    """
    queryset = Slot.objects.none()
    def get(self, request, format=None):
        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CreateSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SlotDetail(APIView):
    """
    Retrieve, update or delete a slot instance.
    """
    queryset = Slot.objects.none()
    def get(self, request, pk, format=None):
        slot = Slot.objects.filter(id=pk)
        if(len(slot) == 0):
            raise Http404
        serializer = SlotSerializer(slot, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Slot.objects.get(id=pk)
        except Slot.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        slot = self.get_object(pk)
        self.check_object_permissions(self.request,slot)
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        slot = self.get_object(pk)
        self.check_object_permissions(self.request,slot)
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SlotListByUser(APIView):
    """
    List all slots, or create a new slot.
    """
    queryset = Reservation.objects.none()
    def get(self, request, format=None):
        slots = Slot.objects.filter(owner=request.user)
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

class ReservedSlotList(APIView):
    """
    List all slots the authenticated user has a reservation for.
    """
    queryset = Slot.objects.none()
    def get(self, request, format=None):
        slots = Slot.objects.none()
        reservations = Reservation.objects.filter(owner=request.user)
        for r in reservations:
            slots |= Slot.objects.filter(id = r.slot.id)
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

################################################################################
################################################################################
# APIView classes for retrieving, creating, and deleting reservations.
################################################################################
################################################################################
class ReservationList(APIView):
    """
    List all reservations, or create a new reservation.
    """
    queryset = Reservation.objects.none()
    def get(self, request, format=None):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CreateReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationListByUser(APIView):
    """
    List all slots, or create a new slot.
    """
    queryset = Reservation.objects.none()
    def get(self, request, format=None):
        reservations = Reservation.objects.filter(owner=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class ReservationDetail(APIView):
    """
    Retrieve, update or delete a reservation instance.
    """
    queryset = Reservation.objects.none()
    def get(self, request, pk, format=None):
        reservation = Reservation.objects.filter(id=pk)
        if(len(reservation) == 0):
            raise Http404
        serializer = ReservationSerializer(reservation, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        print("CALLED " + pk)
        try:
            return Reservation.objects.get(id=pk)
        except Reservation.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        resv = self.get_object(pk)
        self.check_object_permissions(self.request,resv)
        serializer = ReservationSerializer(resv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        resv = self.get_object(pk)
        self.check_object_permissions(self.request,resv)
        resv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReservationDeleteBySlotID(APIView):
    """
    Retrieve, update or delete a reservation instance.
    """
    queryset = Reservation.objects.none()

    def get_object(self, pk):
        print("CALLED " + pk)
        try:
            return Reservation.objects.get(slot=pk)
        except Reservation.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        resv = self.get_object(pk)
        self.check_object_permissions(self.request,resv)
        resv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

################################################################################
################################################################################
# APIView classes for retrieving, creating, and deleting files.
################################################################################
################################################################################
class FileList(APIView):
    """
    List all files, or create a new file.
    """
    queryset = File.objects.none()
    def get(self, request, format=None):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            resv = Reservation.objects.get(id = request.data['reservation'])
            self.check_object_permissions(self.request,resv)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetail(APIView):
    """
    Retrieve or delete a file instance.
    """
    queryset = File.objects.none()
    def get(self, request, pk, format=None):
        file = File.objects.filter(id=pk)
        if(len(file) == 0):
            raise Http404
        serializer = FileSerializer(file, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return File.objects.get(id=pk)
        except File.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        self.check_object_permissions(self.request,file)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
