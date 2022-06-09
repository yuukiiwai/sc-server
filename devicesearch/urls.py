from django.urls import path,include
from .views import *

app_name = 'devicesearch'

urlpatterns = [
    path('',top),
    path('appsatgra/',getAppSat_Gra.as_view(),name='appsatgra')
]