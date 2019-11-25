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

from django.conf.urls import include, url
from django.contrib import admin

from schedule import views

urlpatterns = [
    url(r'^$', views.index),
	url('oauthredirect/', views.oauthredirect),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^scheduleusers/', views.ScheduleUserList.as_view()),
	url(r'^scheduleuser/(?P<pk>[0-9]+)/$', views.ScheduleUserDetail.as_view()),
	url(r'^slots/', views.SlotList.as_view()),
	url(r'^slot/(?P<pk>[0-9]+)/$', views.SlotDetail.as_view()),
	url(r'^reservations/', views.ReservationList.as_view()),
	url(r'^reservation/(?P<pk>[0-9]+)/$', views.ReservationDetail.as_view()),
	url(r'^files/', views.FileList.as_view()),
	url(r'^file/(?P<pk>[0-9]+)/$', views.FileDetail.as_view()),
    url(r'^slot/(?P<slot_id>[0-9]+)/scheduleusers/$', views.ScheduleUsersRegisteredForASlot.as_view()),
]
