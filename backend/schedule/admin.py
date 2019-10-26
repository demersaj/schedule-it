from django.contrib import admin
from .models import User, Reservation, File, Slot

admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(File)
admin.site.register(Slot)
