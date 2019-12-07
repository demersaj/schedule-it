# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

from django.conf.urls import include, url
from django.contrib import admin

from schedule import views
from schedule import info_views

urlpatterns = [
    # views created for explaining the API and creating JSON Web Tokens for testing.
    url(r'^$', info_views.index),
	url('oauthredirect/', info_views.oauthredirect),
	# A backdoor created for testing the API.
    url(r'^admin/', include(admin.site.urls)),
	# Production URLs for the API.
	url(r'^scheduleusers/$', views.ScheduleUserList.as_view()),
	url(r'^scheduleuser/(?P<pk>[0-9]+)/$', views.ScheduleUserDetail.as_view()),
	url(r'^scheduleuser/(?P<onid>[a-z]+)/$', views.ScheduleUserDetailByOnid.as_view()),
	url(r'^slots/$', views.SlotList.as_view()),
	url(r'^slot/(?P<pk>[0-9]+)/$', views.SlotDetail.as_view()),
	url(r'^slots/scheduleuser/$', views.SlotListByUser.as_view()),
	url(r'^reservations/$', views.ReservationList.as_view()),
	url(r'^reservation/slot/(?P<pk>[0-9]+)/$', views.ReservationDeleteBySlotID.as_view()),
	url(r'^reservation/(?P<pk>[0-9]+)/$', views.ReservationDetail.as_view()),
    url(r'^reservations/scheduleuser/$', views.ReservationListByUser.as_view()),
    url(r'^reservations/slots/scheduleuser/$', views.ReservedSlotList.as_view()),
	url(r'^files/$', views.FileList.as_view()),
	url(r'^file/(?P<pk>[0-9]+)/$', views.FileDetail.as_view()),
    url(r'^slot/(?P<slot_id>[0-9]+)/scheduleusers/$', views.ScheduleUsersRegisteredForASlot.as_view()),
]
