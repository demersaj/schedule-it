# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

from django.contrib import admin

from .models import ScheduleUser, Reservation, File, Slot

admin.site.register(ScheduleUser)
admin.site.register(Reservation)
admin.site.register(File)
admin.site.register(Slot)
