from django.db import models

class Student(models.Model):
	onid = models.CharField(
	    'ONID',
	    max_length=25
	)
	first_name = models.CharField(
	    'First name',
	    max_length=50
	)
	last_name = models.CharField(
        'Last name',
        max_length=50
	)
	phone_num = models.CharField(
        'Phone number',
        max_length=25
	)

class Professor(models.Model):
	onid = models.CharField(
	    'ONID',
	    max_length=25
	)
	first_name = models.CharField(
	    'First name',
	    max_length=50
	)
	last_name = models.CharField(
        'Last name',
        max_length=50
	)
	phone_num = models.CharField(
        'Phone number',
        max_length=25
	)
	
class Reservation(models.Model):
	student = models.ForeignKey(
	    'Student',
	    on_delete=models.CASCADE
	)
	slot = models.ForeignKey(
	    'Slot',
	    on_delete=models.CASCADE
	)

class File(models.Model):
	reservation = models.ForeignKey(
	    'Reservation',
	    on_delete=models.CASCADE
	)
	file_name = models.CharField(
	    'File name',
	    max_length=100
    )
	file_type = models.CharField(
	    'File type',
	     max_length=50
	)
	location = models.CharField(
        'File location'
        , max_length=500
	)

class Slot(models.Model):
    date = models.DateField(
        'Date reserved',
        max_length=25
    )
    start_time = models.TimeField(
        'Start time',
        max_length=25
    )
    end_time = models.TimeField(
        'end time',
        max_length=25
    )
    location = models.CharField(
        'location',
        max_length=100
    )
    num_people = models.IntegerField('max number of people')
    created_at = models.DateTimeField(auto_now_add=True)
