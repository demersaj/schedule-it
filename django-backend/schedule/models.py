from django.db import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import datetime
import pytz
from backend import settings
from datetime import date
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission
from django.db import models
# from oauth2client.contrib.django_util.models import CredentialsField

from django.contrib.auth.models import Group

# https://stackoverflow.com/questions/14723099/attributeerror-manager-object-has-no-attribute-get-by-natural-key-error-in
from django.contrib.auth.models import BaseUserManager


def beforeCurrentTime(arg_datetime):
	#print(arg_datetime)
	settings_tz = pytz.timezone(settings.TIME_ZONE)
	current_datetime = datetime.datetime.now(settings_tz)
	#print(current_datetime)
	if(arg_datetime.tzinfo is None or arg_datetime.tzinfo.utcoffset(arg_datetime) is None):
		arg_datetime = settings_tz.localize(arg_datetime)

	return 1 if (current_datetime > arg_datetime) else 0

class ScheduleUserManager(BaseUserManager):
    def create_user(self, onid, password, first_name = 'not set', last_name = 'not set', phone_number = 'not set', creator_privilege = False, is_admin=False, is_staff=False, is_active=True):
        if not onid:
            raise ValueError("User must have an onid")
        if not creator_privilege:
            raise ValueError("User must have creator_privilege set to True or False")

        user = self.model()

        user.onid = onid
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.password = password
        user.creator_privilege = creator_privilege
        user.set_password(password)

        user.admin = False
        user.staff = False
        user.active = True

        user.save(using=self._db)
        return user

    def create_superuser(self, onid, password, first_name = 'not set', last_name = 'not set', phone_number = 'not set', creator_privilege = True, **extra_fields):
        if not onid:
            raise ValueError("User must have an onid")
        if not creator_privilege:
            raise ValueError("User must have creator_privilege set to True or False")

        user = self.model()

        user.onid = onid
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.password = password
        user.creator_privilege = creator_privilege
        user.set_password(password)

        user.admin = True
        user.staff = True
        user.active = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

#from django.contrib.auth.models import User
# https://stackoverflow.com/questions/16349194/django-1-5-understanding-of-abstractbaseuser-and-permissions
class ScheduleUser(AbstractBaseUser, PermissionsMixin):
		# Override the AbstractBaseUser password field.
		# Users will only login through JWTs from Google OAuth2
		#password = None
		# No one should have superuser permissions.
		#is_superuser = None
		onid = models.CharField(
            'ONID',
            max_length=25,
                unique=True,
                null=False
        )
        # ONID is the username.
		USERNAME_FIELD = 'onid'

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
		is_staff = models.BooleanField(
        'is_staff',
		default = False
        )
		def get_short_name(self):
			return self.onid
		objects = ScheduleUserManager()

class Reservation(models.Model):
        owner = models.ForeignKey(
            'scheduleuser',
            on_delete=models.CASCADE,
                null=False
        )
        slot = models.ForeignKey(
            'slot',
            on_delete=models.CASCADE,
                null=False
        )
        class Meta:
                unique_together = ('owner','slot')

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
		'scheduleuser',
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

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Slot, self).save(*args, **kwargs)
