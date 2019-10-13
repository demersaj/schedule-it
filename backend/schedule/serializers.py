from rest_framework import serializers
from .models import Student, Reservation, File, Slot

# convert model instances to JSON so the frontend can work with data

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('onid', 'first_name', 'last_name', 'phone_num')

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('student', 'slot')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('reservation', 'file_name', 'file_type', 'location')

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ('date', 'start_time', 'end_time', 'location', 'num_people')