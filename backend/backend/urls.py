from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from schedule import views


router = routers.DefaultRouter()
router.register(r'students', views.StudentView, 'student')
router.register(r'reservations', views.ReservationView, 'reservation')
router.register(r'files', views.FileView, 'file')
router.register(r'slots', views.SlotView, 'slot')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
