from django.contrib import admin
from .models import Student, Professor, Reservation, File, Slot

admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(Reservation)
admin.site.register(File)
admin.site.register(Slot)
