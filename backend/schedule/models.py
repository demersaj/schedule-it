from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import datetime
import pytz
from backend import settings
from datetime import date

def beforeCurrentTime(arg_date, arg_time):
	settings_tz = pytz.timezone(settings.TIME_ZONE)
	current_datetime = datetime.datetime.now(settings_tz)
	scheduled_datetime = datetime.datetime.combine(arg_date,arg_time)
	scheduled_datetime = settings_tz.localize(scheduled_datetime)

	return 1 if (current_datetime > scheduled_datetime) else 0

class User(models.Model):
        onid = models.CharField(
            'ONID',
            max_length=25,
                unique=True,
                null=False
        )
        first_name = models.CharField(
        'first name',
         max_length=50,
         null=False
        )
        last_name = models.CharField(
        'last name',
        max_length=50,
        null=False
        )
        phone_number = models.CharField(
        'phone number',
        max_length=25,
        null=False
        )
        creator_privilege = models.BooleanField(
        'creator',
        null=False
        )

class Reservation(models.Model):
        user = models.ForeignKey(
            'user',
            on_delete=models.CASCADE,
                null=False
        )
        slot = models.ForeignKey(
            'slot',
            on_delete=models.CASCADE,
                null=False
        )
        class Meta:
                unique_together = ('user','slot')

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
            'reservation',
            on_delete=models.CASCADE,
                null=False
        )
        name = models.CharField(
            'name',
            max_length=100,
                null=False
    )
        type = models.CharField(
            'type',
             max_length=50,
                 null=False
        )
        path = models.CharField(
        'path',
                 max_length=500,
                 null=False
        )
        class Meta:
                unique_together = ('name','path')

class Slot(models.Model):

    StartTime = models.DateTimeField(
        'start time',
        max_length=50,
		null=False
    )

    EndTime = models.DateTimeField(
        'end time',
        max_length=50,
		null=False
    )

    Location = models.CharField(
		'location',
		max_length=100,
		null=False
	)

    Owner = models.ForeignKey(
		'user',
		on_delete=models.CASCADE,
			null=False
	)

    Subject = models.CharField(
	    'subject',
	    max_length=100
	)


    def clean(self):
        if self.StartTime > self.EndTime:
             raise APIException(detail='Start time must be before end time.',code='400')
#         if(beforeCurrentTime(date.today(), self.start_time)):
#             raise APIException(detail='Time Slots can\'t be created in the the past.',code='400')
#         if(self.creator.creator_privilege == False):
#             raise APIException(detail='Time Slots can\'t be created by this user.',code='400')


    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Slot, self).save(*args, **kwargs)
