from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, ReservationSerializer, FileSerializer, SlotSerializer
from .models import User, Reservation, File, Slot
from django.shortcuts import render_to_response, redirect, render
import httplib2
from googleapiclient.discovery import build
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponse,
)
from .models import CredentialsModel
from backend import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from django.shortcuts import render
from httplib2 import Http

#Added for APIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

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

# @api_view(['GET', 'DELETE', 'POST'])
# def slotDetail(request, StartDate, EndDate):
#     try:
#         slot = Slot.objects.get(start_time=startDate)
#     except Slot.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = SlotSerializer(slot, context={'request': request})
#         return Response(serializer.data)

class ReservationList(APIView):
    """
    List all reservations, or create a new reservation.
    """
    def get(self, request, format=None):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetail(APIView):
    """
    Retrieve, update or delete a reservation instance.
    """
    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        resv = self.get_object(pk)
        serializer = ReservationSerializer(resv)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        resv = self.get_object(pk)
        serializer = ReservationSerializer(resv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        resv = self.get_object(pk)
        resv.delete()
        print("DELETE RESERVATION CALLED")
        return Response(status=status.HTTP_204_NO_CONTENT)

class SlotList(APIView):
    """
    List all slots, or create a new slot.
    """
    def get(self, request, format=None):
        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SlotDetail(APIView):
    """
    Retrieve, update or delete a slot instance.
    """
    def get_object(self, pk):
        try:
            return Slot.objects.get(pk=pk)
        except Slot.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        slot = self.get_object(pk)
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        slot = self.get_object(pk)
        slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserList(APIView):
    """
    List all users, or create a new user.
    """
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
        	serializer.save()
        	return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FileList(APIView):
    """
    List all files, or create a new file.
    """
    def get(self, request, format=None):
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetail(APIView):
    """
    Retrieve, update or delete a file instance.
    """
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        file = self.get_object(pk)
        serializer = FileSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SlotListByOnid(APIView):
    """
    List all slots with an onid, or create a new slot.
    """
    queryset = Slot.objects.none()
    def get(self, request, onid, format=None):
        user_id = User.objects.get(onid=onid)
        slots = Slot.objects.filter(owner=user_id)
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

class ReservationListByOnid(APIView):
    """
    List all slots, or create a new slot.
    """
    queryset = Reservation.objects.none()
    def get(self, request, onid, format=None):
        user_id = ScheduleUser.objects.get(onid=onid)
        reservations = Reservation.objects.filter(user=user_id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

def logout(request):
    auth_logout(request)
    return redirect('/')

################################
#   GMAIL API IMPLEMENTATION   #
################################

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://apis.google.com/js/platform.js',
    redirect_uri='http://localhost:8000/oauth2callback',
    prompt='consent')

def authenticate(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('gmail', 'v1', http=http)
        print('access_token = ', credential.access_token)
        status = True

        response = HttpResponse("User authenticated")
        return response


def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    print("access_token: %s" % credential.access_token)

    response = HttpResponse("User authenticated")
    return response
