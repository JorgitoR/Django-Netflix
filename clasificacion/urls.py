from django.urls import path 

from .views import clasificar_object_view

urlpatterns = [

	path('object-rate/', clasificar_object_view)
]