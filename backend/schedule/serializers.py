from rest_framework import serializers
from .models import Student, Reservation, File, Slot

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('onid', 'first_name', 'last_name', 'phone_num')

