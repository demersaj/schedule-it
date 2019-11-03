from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import datetime
import pytz
from backend import settings
from datetime import date
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField


class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key = True, on_delete = models.CASCADE)
    credential = CredentialsField()
    task = models.CharField(max_length = 80, null = True)
    updated_time = models.CharField(max_length = 80, null = True)


class CredentialsAdmin(admin.ModelAdmin):
    pass

def beforeCurrentTime(arg_datetime):
	settings_tz = pytz.timezone(settings.TIME_ZONE)
	current_datetime = datetime.datetime.now(settings_tz)
	if(arg_datetime.tzinfo is None or arg_datetime.tzinfo.utcoffset(arg_datetime) is None):
		arg_datetime = settings_tz.localize(arg_datetime)

	return 1 if (current_datetime > arg_datetime) else 0


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

            if(beforeCurrentTime(self.slot.start)):
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

    start = models.DateTimeField(
        'start time',
        max_length=50,
		null=False
    )

    end = models.DateTimeField(
        'end time',
        max_length=50,
		null=False
    )

    location = models.CharField(
		'location',
		max_length=100,
		null=False
	)

    owner = models.ForeignKey(
		'user',
		on_delete=models.CASCADE,
			null=False
	)

    title = models.CharField(
	    'title',
	    max_length=100
	)

    num_people = models.IntegerField('max number of people')


    def clean(self):
        print(self.start)
        print(self.end)
        if self.start > self.end:
             raise APIException(detail='Start time must be before end time.',code='400')
        if(beforeCurrentTime(self.start)):
             raise APIException(detail='Time Slots can\'t be created in the the past.',code='400')
#         if(self.creator.creator_privilege == False):
#             raise APIException(detail='Time Slots can\'t be created by this user.',code='400')


    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Slot, self).save(*args, **kwargs)
