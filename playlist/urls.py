from django.urls import path

from .views import (

	PeliculaListaView,
	TVSHOWListView, 
	PlayListDestacadoView,
	
	PeliculaDetailView,
	PlaylistDetailView,
	TVShowDetailView,
	TVShowTemporadaDetailView
)

urlpatterns = [

	path('', PlayListDestacadoView.as_view(), name='PlayListDestacadoView'),
	path('movie', PeliculaListaView.as_view(), name='PeliculaListaView'),
	path('show/', TVSHOWListView.as_view(), name='TVSHOWListView'),


	path('pelicula/<slug:slug>/', PeliculaDetailView.as_view(), name='PeliculaDetailView'),
	
	path('media/<int:pk>', PlaylistDetailView.as_view(), name='PlaylistDetailView'),


    path('shows/<slug:slug>/seasons/', TVShowDetailView.as_view()),
    path('shows/<slug:slug>/', TVShowDetailView.as_view()),

    
    path('shows/<slug:showSlug>/seasons/<slug:seasonSlug>/', TVShowTemporadaDetailView.as_view()),

]