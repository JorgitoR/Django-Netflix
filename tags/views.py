from django.shortcuts import render

from django.views import View 

from .models import TaggedItem

from django.views.generic import DetailView, ListView
from playlist.mixins import PlayListMixin


from playlist.models import PlayList

class TaggedItemListView(View): #it's something like FBV
	def get(self, request):
		#tags = TaggedItem.objects.all().valuest_list('tag', flat=True)
		tag_list = TaggedItem.objects.lista_unica()
		context = {

			'tags':tag_list

		}

		return render(request, 'tags/lista.html', context)

class TaggedItemDetailView(PlayListMixin, ListView):

	def get_context_data(self):
		context = super().get_context_data()
		context['titulo'] = f"{self.kwargs.get('tag')}".title()
		return context

	def get_queryset(self):
		tag = self.kwargs.get('tag')
		return PlayList.objects.filter(tags__tag=tag).pelicula_o_show()