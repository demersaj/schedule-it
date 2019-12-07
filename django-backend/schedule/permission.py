# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from schedule.models import ScheduleUser, Reservation, File, Slot, beforeCurrentTime
from rest_framework import exceptions

class CustomObjectPermission(DjangoModelPermissions):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    authenticated_users_only = True
    def has_object_permission(self, request, view, obj):
        #print("has_object_permission called")
        if type(obj) == Slot:
            return self.slot_object_permission(request, view, obj)
        if type(obj) == Reservation:
            return self.reservation_object_permission(request, view, obj)
        if type(obj) == File:
            return self.file_object_permission(request, view, obj)

    def slot_object_permission(self, request, view, obj):
        #print("slot_object_permission called")
        if obj.owner != request.user:
            raise exceptions.PermissionDenied('Permission Denied: Slot owner and user do not match.')
        if beforeCurrentTime(obj.end):
            raise exceptions.PermissionDenied('Permission Denied: Slots can\'t be modified or deleted after they end.')
        return True

    def reservation_object_permission(self, request, view, obj):
        #print("reservation_object_permission called")
        if obj.owner != request.user:
            raise exceptions.PermissionDenied('Permission Denied: Reservation owner and user do not match.')
        if beforeCurrentTime(obj.slot.end):
            raise exceptions.PermissionDenied('Permission Denied: Reservations can\'t be modified or deleted after the slot ended.')
        return True

    def file_object_permission(self, request, view, obj):
        #print("file_object_permission called")
        if obj.reservation.owner != request.user:
            raise exceptions.PermissionDenied('Permission Denied: File owner and user do not match.')
        if beforeCurrentTime(obj.reservation.slot.end):
            raise exceptions.PermissionDenied('Permission Denied: Files can\'t be deleted after the slot ended.')
        return True
