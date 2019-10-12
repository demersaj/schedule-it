from django.contrib import admin
from .models import Student, Reservation, File, Slot

admin.site.register(Student)
admin.site.register(Reservation)
admin.site.register(File)
admin.site.register(Slot)
