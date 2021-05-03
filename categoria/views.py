from django.shortcuts import render

from django.views.generics import ListView, DetailView

from .models import categoria

from django.http import Htpp404

from django.db.models import Count

from playlist.models import PlayList
from playlist.mixins import PlayListMixin


class CategoriaListView(ListView):
	queryset = categoria.objects.all().filter(activo=True).annotate(pl_count=Count('playlist__set')).filter(pl_count__gt=0)


class CategoriaDetailView(PlayListMixin, ListView):
	"""
		Otra ListView para PlayList
	"""


	def get_context_data(self):
		context = super().get_context_data()
		try:
			obj = categoria.objects.get(slug=self.kwargs.get('slug'))
		except categoria.DoesNotExist:
			raise Htpp404
		except categoria.MultipleObjectsReturned:
			raise Htpp404
		except:
			obj None

		context['object'] = obj 
		if obj is not None:
			context['titulo'] = obj.titulo
		return context

	def get_queryset(self):
		slug = self.kwargs.get("slug")
		return PlayList.objects.filter(categoria__slug=slug)