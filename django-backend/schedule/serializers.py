from rest_framework import serializers
from schedule.models import ScheduleUser, Reservation, File, Slot

# convert model instances to JSON so the frontend can work with data

class ScheduleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleUser
        fields = '__all__'
        many = True

class ReservationSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Slot
        fields = '__all__'
        many = True
