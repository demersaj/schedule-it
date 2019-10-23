from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from schedule import views


router = routers.DefaultRouter()
router.register(r'Users', views.UserView, 'User')
router.register(r'Reservations', views.ReservationView, 'Reservation')
router.register(r'Files', views.FileView, 'File')
router.register(r'Slots', views.SlotView, 'Slot')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
