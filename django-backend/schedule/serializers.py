# CS467 Fall 2019
# Schedule-It
# Decision to use and initial setup for django, django-rest-framework, and database models Andrew Demers.
# Constraints, permissions, authentication, google app engine hosting, more specific API functions by Nathan Crozier.

from rest_framework import serializers
from schedule.models import ScheduleUser, Reservation, File, Slot

# convert model instances to JSON so the frontend can work with data

class ScheduleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleUser
        fields = ['id','onid','first_name','last_name']
        many = True

class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        many = True

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        many = True

class SlotSerializer(serializers.ModelSerializer):
    owner = ScheduleUserSerializer()
    class Meta:
        model = Slot
        fields = '__all__'
        depth = 1
        many = True

class CreateSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'
        many = True

class ReservationSerializer(serializers.ModelSerializer):
    owner = ScheduleUserSerializer()
    slot = SlotSerializer()
    class Meta:
        model = Reservation
        fields = '__all__'
        many = True

class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        many = True
