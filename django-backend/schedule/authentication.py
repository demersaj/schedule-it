# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

#Added for django-rest-framework Authentication.
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from schedule.models import ScheduleUser, Reservation, File, Slot
import json
from google.oauth2 import id_token
from google.auth.transport import requests
from backend.settings import client_id, client_secret

class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
		# Step 0: check for Authorization header.
		# Deny the request without it or the field is blank.
        if('HTTP_AUTHORIZATION') not in request.META:
            return None
        if(request.META['HTTP_AUTHORIZATION'] == ''):
            return None

		# Step 1: Split the header field by whitespace.
        tokenHeader = request.META['HTTP_AUTHORIZATION']
        tokenHeader = tokenHeader.split()

		# Step 2: Check if there are two parts.
        if(len(tokenHeader) != 2):
            return None

		# Step 3: Check that the first word is Bearer.
        if tokenHeader[0] != 'Bearer':
            return None

		# Step 4: Get the JWT and set it to token.
        token = tokenHeader[1]

		# Step 5: Verify the token and retieve the ONID/username.
		# If the JWT is invalid, raise AuthenticationFailed exception.
		# If the ONID is not in the table, raise AuthenticationFailed exception.
        try:
            req = requests.Request()
            id_info = id_token.verify_oauth2_token(token, req, client_id)

            onid = id_info['email'].split('@')[0]
            if id_info['email'].split('@')[1] != 'oregonstate.edu':
                raise exceptions.AuthenticationFailed('Only oregonstate.edu email addresses are allowed.')
            user = ScheduleUser.objects.get(onid=onid)
            if user.phone_number == 'not set':
                 user.phone_number = id_info['sub']
            elif user.phone_number != id_info['sub']:
                raise exceptions.AuthenticationFailed("sub value does not match account in database. Delete and recreate the user in database.")
			# This will sync the name fields of the user in the database with their Oregon State University/Google Account.
            if 'given_name' in id_info and 'family_name' in id_info:
            	if id_info['given_name'] != user.first_name:
                	user.first_name = id_info['given_name']
            	if id_info['family_name'] != user.last_name:
                	user.last_name = id_info['family_name']
            	user.save()
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

		# Step 6: If the request is POST or PUT, add
		# the user.id authenticated to the owner field.
        if request.method == 'POST' or request.method == 'PUT':
            if request.body == b'':
                raise exceptions.ValidationError('POST and PUT requests require a body.')
            jsonBody = json.loads(request.body)
            jsonBody['owner'] = user.id
            request.body = bytearray(json.dumps(jsonBody),'utf-8')

		# Step 7: Return the authenticated user.
		# At this point request.user is automatically set to the authenticated user.
        return (user,None)
