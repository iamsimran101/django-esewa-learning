from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('buy/<int:id>/', buy, name='buy'),
    path('success/<int:id>/', success, name='success'),
    path('failure/<int:id>/', failure, name='failure'),

]
