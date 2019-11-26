# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse

# Added for Google OAuth2
from requests_oauthlib import OAuth2Session
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
import requests
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

# These should be copied from an OAuth2 Credential section at
# https://console.cloud.google.com/apis/credentials
client_id = r'removed'
client_secret = r'removed'

# This is the page that you will use to decode and collect the info from
# the Google authentication flow
#redirect_uri = 'https://127.0.0.1:8000/oauthredirect/'
redirect_uri = 'https://cs467-backend-nc.appspot.com/oauthredirect/'

# These let us get basic info to identify a user and not much else
# they are part of the Google People API
scope = ['https://www.googleapis.com/auth/userinfo.email',
             'https://www.googleapis.com/auth/userinfo.profile', 'openid']
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=scope)

#Added for APIView
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from schedule.models import ScheduleUser, Reservation, File, Slot
from schedule.serializers import ScheduleUserSerializer, ReservationSerializer, FileSerializer, SlotSerializer

intro ="""
<h1>Can, do. You're at the schedule-it! index.</h1>
<p>Here are the URLs for the REST API and what they do:</p>
<h2>GET Requests</h2>
<p><a href=/scheduleusers/>/scheduleusers/</a> returns a list of all the schedulerusers</p>
<p><a href=/slots/>/slots/</a> returns a list of all the slots</p>
<p><a href=/reservations/>/reservations/</a> returns a list of all the reservations</p>
<p><a href=/files/>/files/</a> returns a list of all the files</p>
<p><a href=/slot/1/scheduleusers/>/slot/{slot_id}/scheduleusers/</a> returns a list of all ScheduleUsers registered for a slot.</p>
<p><a href=/scheduleuser/slots>/scheduleuser/slots/</a> returns a list a slots created by the authenticated user.</p>
<p><a href=/scheduleuser/reservations>/scheduleuser/reservations/</a> returns a list a reservations created by the authenticated user.</p>
<p><a href=/scheduleuser/1/>/scheduleuser/{scheduleuser_id}/</a> returns a scheduleruser with {scheduleuser_id}</p>
<p><a href=/slot/1/>/slot/{slot_id}/</a> returns a slot with {slot_id}</p>
<p><a href=/reservation/1/>/reservation/{resrvation_id}</a> returns a reservations with {reservation_id}</p>
<p><a href=/file/1/>/file/{file_id}/</a> returns a file with {file_id}</p>

<h2>POST Requests</h2>
<p><a href=/scheduleusers/>/scheduleusers/</a> is not used a security feature. Users can only be created with manage.py createuser or createsuperuser. In the final version there will be no superusers.</p>
<p><a href=/slots/>/slots/</a> creates a slot if the user has permission to create a timeslot.</p>
<p><a href=/reservations/>/reservations/</a> creates a reservation if the slot is not filled and there isn't a conflict with an existing reservation.</p>
<p><a href=/files/>/files/</a> creates a file associated with a reservation.</p>
<h2>PUT Requests</h2>
<p><a href=/scheduleusers/>/scheduleusers/</a> is not used a security feature. Users can not change their names or privileges.</p>
<p><a href=/slots/>/slots/</a> is only be used to change a timeslots name or description.</p>
<p><a href=/reservations/>/reservations/</a> is not used. Reservations can only be created an deleted.</p>
<p><a href=/files/>/files/</a> is not used. Files can only be created an deleted.</p>
<h2>DELETE Requests</h2>
<p><a href=/scheduleusers/>/scheduleusers/</a> is not used a security feature. </p>
<p><a href=/slots/>/slots/</a> can only be used by the user who created the slot.</p>
<p><a href=/reservations/>/reservations/</a> can only be used by the user who created the reservation.</p>
<p><a href=/files/>/files/</a> can only be used by the user who created the file.</p>
<p><i>*permissions and authentication are currently enforced.</i></p>
"""


def index(request):
    authorization_url, state = oauth.authorization_url('https://accounts.google.com/o/oauth2/auth',access_type="offline", prompt="select_account",include_granted_scopes='true')
    a = "<p>Here's the URL to get a JWT for the API: <a href=" + authorization_url + ">Login to Google</a></p>"
    return HttpResponse(intro + a)

def oauthredirect(request):
	try:
		token = oauth.fetch_token('https://accounts.google.com/o/oauth2/token',client_id=client_id,client_secret=client_secret, authorization_response=request.get_raw_uri())
		req = requests.Request()
		#id_info = id_token.verify_oauth2_token(token['id_token'], req, client_id)
		JWT = token['id_token']
	except Exception as e:
	 	return HttpResponse("OAuth Redirect Failed: " +str(e))
	authorization_url, state = oauth.authorization_url('https://accounts.google.com/o/oauth2/auth',access_type="offline", prompt="select_account")
	a = "<p>Here's the URL to get a JWT for the API: <a href=" + authorization_url + ">Login to Google</a></p>"
	b = "<p>Here's your JWT for the API: " + JWT + "</p>"
	return HttpResponse(intro + a + b)

class ScheduleUserList(APIView):
    """
    List all users, or create a new user.
    """
    queryset = ScheduleUser.objects.none()
    def get(self, request, format=None):
        users = ScheduleUser.objects.all()
        serializer = ScheduleUserSerializer(users , many=True)
        return Response(serializer.data)

class ScheduleUserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    queryset = ScheduleUser.objects.none()
    def get_object(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = ScheduleUserSerializer(user)
        return Response(serializer.data)

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
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SlotDetail(APIView):
    """
    Retrieve, update or delete a slot instance.
    """
    queryset = Slot.objects.none()
    def get_object(self, pk):
        try:
            return Slot.objects.get(pk=pk)
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
        #user_id = ScheduleUser.objects.get(owner=request.user)
        slots = Slot.objects.filter(owner=request.user)
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

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
        serializer = ReservationSerializer(data=request.data)
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
        #user_id = ScheduleUser.objects.get(owner=request.user)
        reservations = Reservation.objects.filter(owner=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class ReservationDetail(APIView):
    """
    Retrieve, update or delete a reservation instance.
    """
    queryset = Reservation.objects.none()
    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
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
        print("DELETE RESERVATION CALLED")
        return Response(status=status.HTTP_204_NO_CONTENT)

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetail(APIView):
    """
    Retrieve or delete a file instance.
    """
    queryset = File.objects.none()
    def get_object(self, pk):
        try:
            return File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        file = self.get_object(pk)
        self.check_object_permissions(self.request,file)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ScheduleUsersRegisteredForASlot(APIView):
    """
    List all users registered for a slot.
    """
    queryset = ScheduleUser.objects.none()
    def get(self, request, slot_id, format=None):
        print("Called")
        reservations = Reservation.objects.filter(slot=slot_id)
        users = ScheduleUser.objects.none()
        for r in reservations:
            users |= ScheduleUser.objects.filter(id = r.owner.id)
        serializer = ScheduleUserSerializer(users , many=True)
        return Response(serializer.data)
