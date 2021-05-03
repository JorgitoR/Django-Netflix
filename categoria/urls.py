from django.urls import path

from .views import (

	CategoriaListView,
	CategoriaDetailView

	)

urlpatterns = [

	path('categorias/', CategoriaListView.as_view()),
	path('<slug:slug>/', CategoriaDetailView.as_view())

]