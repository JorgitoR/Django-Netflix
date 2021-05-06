from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import MovieProxy, TVShowProxy, PlayList, TVShowTemporadaProxy

from .mixins import PlayListMixin

from django.utils import timezone

from django.http import Http404


from NetFlix.db.models import PublishStateOptions


class BuscarView(PlayListMixin, ListView):

	def get_context_data(self):
		context = super().get_context_data()
		query = self.request.GET.get("q")
		if query is not None:
			context['titulo'] = f"Buscar por {query}"
		else:
			context["titulo"] = "Buscando..."

		return context

	def get_queryset(self):
		query = self.request.GET.get("q") #request.GET = {}
		return PlayList.objects.all().pelicula_o_show().buscador(query=query)

class PeliculaListaView(PlayListMixin, ListView):
	queryset = MovieProxy.objects.all()
	titulo ="Peliculas"

class PeliculaDetailView(PlayListMixin, DetailView):
	template_name = 'playlist/pelicula_detail.html'
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

		try:
			obj = TVShowTemporadaProxy.objects.get(

				stado = PublishStateOptions.PUBLISH,
				tiempo_publicado__lte = ahora,
				padre__slug__iexact = show_slug,
				slug__iexact = temporada_slug

			)

		except TVShowTemporadaProxy.MultipleObjectsReturned:
			qs = TVShowTemporadaProxy.objects.filter(

				padre__slug__iexact =show_slug,
				slug__iexact = temporada_slug
			)
			obj = qs.first()

		except:
			raise Http404

		return obj
		#print(show_slug, temporada_slug)
		#qs = self.get_queryset().filter(padre__slug__iexact=show_slug, slug__iexact=temporada_slug)
		#if not qs.count() == 1:
		#	raise Http404
		#return qs.first()


class PlayListDestacadoView(PlayListMixin, ListView):
	template_name = 'playlist/lista_destacada.html'
	queryset = PlayList.objects.playlist_destacados()
	titulo = 'Destacado'



#Nuestro mixin es reemplazado por las funcionalidades agregadas
#a nuestra clase, es decir, si socreescribimos un queryset, este sera
#el queryset final, reemplazara el del mixin

class PlaylistDetailView(PlayListMixin, DetailView):
    template_name = 'playlist/playlist_detail.html'
    queryset = PlayList.objects.all()

    def get_object(self):
    	request = self.request
    	kwargs = self.kwargs
    	print(request, kwargs)
    	
    	return self.get_queryset().filter(**kwargs).first()
    	#return self.get_queryset().first() Con este codigo devuelvo el primer elemento