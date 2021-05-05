from django.urls import path

from .views import TaggedItemListView

urlpatterns = [

	path('tags/', TaggedItemListView.as_view())

]