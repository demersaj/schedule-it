from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from schedule import views


router = routers.DefaultRouter()
router.register(r'users', views.UserView, 'User')
router.register(r'reservations', views.ReservationView, 'Reservation')
router.register(r'files', views.FileView, 'File')
router.register(r'slots', views.SlotView, 'Slot')

urlpatterns = [
    path('', include('frontend.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
