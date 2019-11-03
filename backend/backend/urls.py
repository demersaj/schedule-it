from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from schedule import views
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register(r'users', views.UserView, 'User')
router.register(r'reservations', views.ReservationView, 'Reservation')
router.register(r'files', views.FileView, 'File')
router.register(r'slots', views.SlotView, 'Slot')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('schedule.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('api/', include(router.urls)),
	path('reservations/', views.ReservationList.as_view()),
    path('reservations/<int:pk>/', views.ReservationDetail.as_view()),
    path('slots/<int:pk>/', views.SlotDetail.as_view()),
	path('slots/', views.SlotList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
	path('users/', views.UserList.as_view()),
    path('files/<int:pk>/', views.FileDetail.as_view()),
	path('files/', views.FileList.as_view()),
]
