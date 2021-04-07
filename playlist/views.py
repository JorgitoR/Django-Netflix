from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import MovieProxy, TVShowProxy, PlayList, TVShowTemporadaProxy

from .mixins import PlayListMixin

from django.utils import timezone

from django.http import Http404

class PeliculaListaView(PlayListMixin, ListView):
	queryset = MovieProxy.objects.all()
	titulo ="Peliculas"

class PeliculaDetailView(PlayListMixin, DetailView):
	template_name= 'playlist/Pelicula_detail.thml'
	queryset = MovieProxy.objects.all()


class TVSHOWListView(PlayListMixin, ListView):
	queryset = TVShowProxy.objects.all()
	titulo = 'Tv Shows'

class TVShowDetailView(PlayListMixin, DetailView):
	template_name = 'playlist/tvshow_detail.html'
	queryset = TVShowProxy.objects.all()


class TVShowTemporadaDetailView(PlayListMixin, DetailView):
	template_name = 'playlist/temporada_detail.html'
	queryset = TVShowTemporadaProxy.objects.all()

	def get_object(self):
		kwargs = self.kwargs
		show_slug = kwargs.get("showSlug")
		temporada_slug = kwargs.get("seasonSlug")
		ahora = timezone.now()

		qs = self.get_queryset().filter(padre__slug__iexact=show_slug, slug__iexact= temporada_slug)
		if not qs.count() == 1:
			raise Http404
		return qs.first()


class PlayListDestacadoView(PlayListMixin, ListView):
	template_name = 'playlist/lista_destacada.html'
	queryset = PlayList.objects.playlist_destacados()
	titulo = 'Destacado'



class PlaylistDetailView(PlayListMixin, DetailView):
    template_name = 'playlist/playlist_detail.html'
    queryset = PlayList.objects.all()

    def get_object(self):
    	request = self.request
    	kwargs = self.kwargs
    	print(request, kwargs)
    	return self.get_queryset().filter(**kwargs).first()