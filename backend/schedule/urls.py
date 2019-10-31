from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^auth', views.authenticate, name='authenticate'),
    url(r'^oauth2callback', views.auth_return),
]
