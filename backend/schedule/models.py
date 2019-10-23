from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import datetime
import pytz
from backend import settings

def beforeCurrentTime(arg_date,arg_time):
	settings_tz = pytz.timezone(settings.TIME_ZONE)
	current_datetime = datetime.datetime.now(settings_tz)
	scheduled_datetime = datetime.datetime.combine(arg_date,arg_time)
	scheduled_datetime = settings_tz.localize(scheduled_datetime)

	if(current_datetime > scheduled_datetime):
		return 1
	else:
		return 0


class Student(models.Model):
        onid = models.CharField(
            'ONID',
            max_length=25,
                unique=True,
                null=False
        )
        first_name = models.CharField(
            'First name',
            max_length=50,
                null=False
        )
        last_name = models.CharField(
        'Last name',
        max_length=50,
                null=False
        )
        phone_num = models.CharField(
        'Phone number',
        max_length=25,
                null=False
        )

class Professor(models.Model):
        onid = models.CharField(
            'ONID',
            max_length=25,
                unique=True,
                null=False
        )
        first_name = models.CharField(
            'First name',
            max_length=50,
                null=False
        )
        last_name = models.CharField(
        'Last name',
        max_length=50,
                null=False
        )
        phone_num = models.CharField(
        'Phone number',
        max_length=25,
                null=False
        )

class Reservation(models.Model):
        student = models.ForeignKey(
            'Student',
            on_delete=models.CASCADE,
                null=False
        )
        slot = models.ForeignKey(
            'Slot',
            on_delete=models.CASCADE,
                null=False
        )
        class Meta:
                unique_together = ('student','slot')

        def clean(self):
            if self.slot.num_people <= len(Reservation.objects.filter(slot_id = self.slot_id)):
                raise APIException(detail='The slot is filled.',code='400')

            if(beforeCurrentTime(self.slot.date,self.slot.start_time)):
	            raise APIException(detail='Reservations can\'t be made for time slots in the the past.',code='400')

        def save(self, *args, **kwargs):
            self.full_clean()
            return super(Reservation, self).save(*args, **kwargs)


class File(models.Model):
        reservation = models.ForeignKey(
            'Reservation',
            on_delete=models.CASCADE,
                null=False
        )
        file_name = models.CharField(
            'File name',
            max_length=100,
                null=False
    )
        file_type = models.CharField(
            'File type',
             max_length=50,
                 null=False
        )
        location = models.CharField(
        'File location',
                 max_length=500,
                 null=False
        )
        class Meta:
                unique_together = ('file_type','location')

class Slot(models.Model):
    date = models.DateField(
        'Date reserved',
        max_length=25,
		null=False
    )

    start_time = models.TimeField(
        'Start time',
        max_length=25,
		null=False
    )

    end_time = models.TimeField(
        'end time',
        max_length=25,
		null=False
    )

    location = models.CharField(
		'location',
		max_length=100,
		null=False
	)

    num_people = models.IntegerField('max number of people')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.start_time > self.end_time:
             raise APIException(detail='Start time must be before end time.',code='400')

        if(beforeCurrentTime(self.date,self.start_time)):
            raise APIException(detail='Time slots can\'t be created in the the past.',code='400')


    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Slot, self).save(*args, **kwargs)
