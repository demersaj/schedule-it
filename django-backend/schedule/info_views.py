# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

# Needed for sending HttpResponse's with django.
from django.http import HttpResponse

# Added for Google OAuth2
from requests_oauthlib import OAuth2Session
from google.oauth2 import id_token
from google.auth import crypt
from google.auth import jwt
from google.auth.transport import requests
import requests
from backend.settings import client_id, client_secret, redirect_uri, scope

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri,scope=scope)

intro ="""
<h1>You're at the schedule-it! API index.</h1>
<p>Here are the URLs for the REST API and what they do:</p>

<h2>GET Requests</h2>
<p><a href=/scheduleusers/>/scheduleusers/</a> returns a list of all the schedulerusers</p>
<p><a href=/slots/>/slots/</a> returns a list of all the slots</p>
<p><a href=/reservations/>/reservations/</a> returns a list of all the reservations</p>
<p><a href=/files/>/files/</a> returns a list of all the files</p>
<p><a href=/slot/1/scheduleusers/>/slot/{slot_id}/scheduleusers/</a> returns a list of all ScheduleUsers registered for a slot.</p>
<p><a href=/slots/scheduleuser/>/slots/scheduleuser/</a> returns a list a slots created by the authenticated user.</p>
<p><a href=/reservations/scheduleuser/>/reservations/scheduleuser/</a> returns a list a reservations created by the authenticated user.</p>
<p><a href=/reservations/slots/scheduleuser/>/reservations/slots/scheduleuser/</a> returns a list of slots the authenticated user has a reservation for.</p>
<p><a href=/scheduleuser/1/>/scheduleuser/{scheduleuser_id}/</a> returns a scheduleruser with {scheduleuser_id}</p>
<p><a href=/scheduleuser/1/>/scheduleuser/{onid}/</a> returns a scheduleruser with {onid}</p>
<p><a href=/slot/{slot_id}/>/slot/{slot_id}/</a> returns a slot with {slot_id}</p>
<p><a href=/reservation/{resrvation_id}/>/reservation/{resrvation_id}</a> returns a reservations with {reservation_id}</p>
<p><a href=/file/{file_id}/>/file/{file_id}/</a> returns a file with {file_id}</p>

<h2>POST Requests</h2>
<p><a href=/scheduleusers/>/scheduleusers/</a> is not used a security feature. Users can only be created with manage.py createuser or createsuperuser. In the final version there will be no superusers.</p>
<p><a href=/slots/>/slots/</a> creates a slot if the user has permission to create a timeslot.</p>
<p><a href=/reservations/>/reservations/</a> creates a reservation if the slot is not filled and there isn't a conflict with an existing reservation.</p>
<p><a href=/files/>/files/</a> creates a file associated with a reservation.</p>

<h2>PUT Requests</h2>
<p>scheduleusers can not be changed through the API as a security feature.</p>
<p><a href=/slot/{slot_id}/>/slot/{slot_id}/</a> should only be used to change a slots name or description.</p>
<p>Reservations can only be created an deleted.</p>
<p>Files can only be created an deleted.</p>

<h2>DELETE Requests</h2>
<p>scheduleusers can not be deleted through the API as a security feature.</p>
<p><a href=/slot/{slot_id}/>/slot/{slot_id}/</a> can only be used by the user who created the slot.</p>
<p><a href=/reservation/{reservation_id}/>/reservation/{reservation_id}/</a> can only be used by the user who created the reservation.</p>
/reservation/slot/{slot_id}/ deletes the reservation for the authenticated user for the slot with {slot_id}.
<p><a href=/file/{file_id}/>/file/{file_id}/</a> can only be used by the user who created the file.</p>
<p><i>*permissions and authentication are currently enforced.</i></p>
"""


def index(request):
	if 'oauth_token' not in request.session:
		request.session['oauth_token'] = None
	authorization_url, state = oauth.authorization_url('https://accounts.google.com/o/oauth2/v2/auth',access_type="offline", prompt="select_account",include_granted_scopes='true')
	token_url_html = "<p>Here's the URL to get a JWT for the API: <a href=" + authorization_url + ">Login to Google</a></p>"
	if request.session['oauth_token'] == None:
		return HttpResponse(intro + token_url_html)
	else:
		retrieved_token_html = "<p>Here's your JWT for the API: " + request.session['oauth_token'] + "</p>"
		return HttpResponse(intro + token_url_html + retrieved_token_html)

def oauthredirect(request):
	try:
		token = oauth.fetch_token('https://www.googleapis.com/oauth2/v4/token',client_id=client_id,client_secret=client_secret, authorization_response=request.get_raw_uri())
		req = requests.Request()
		JWT = token['id_token']
	except Exception as e:
	 	return HttpResponse("OAuth Redirect Failed: " +str(e))
	request.session['oauth_token'] = JWT
	response = HttpResponse(content="", status=303)
	response["Location"] = 'https://' + request.META['HTTP_HOST']
	return response
