from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import categoria

from django.http import Http404

from django.db.models import Count

from playlist.models import PlayList
from playlist.mixins import PlayListMixin


class CategoriaListView(ListView):
	queryset = categoria.objects.all().filter(activo=True).annotate(pl_count=Count('playlist')).filter(pl_count__gt=0)


class CategoriaDetailView(PlayListMixin, ListView):
	"""
		Otra ListView para PlayList
	"""


	def get_context_data(self):
		context = super().get_context_data()
		try:
			obj = categoria.objects.get(slug=self.kwargs.get('slug'))
		except categoria.DoesNotExist:
			raise Http404
		except categoria.MultipleObjectsReturned:
			raise Http404
		except:
			obj =  None

		context['object'] = obj 
		if obj is not None:
			context['titulo'] = obj.titulo
		return context

	def get_queryset(self):
		slug = self.kwargs.get("slug")
		return PlayList.objects.filter(categoria__slug=slug).pelicula_o_show()