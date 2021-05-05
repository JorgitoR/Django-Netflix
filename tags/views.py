from django.shortcuts import render

from django.views import View 

from .models import TaggedItem

class TaggedItemListView(View): #it's something like FBV
	def get(self, request):
		tag_list = TaggedItem.objects.lista_unica()
		context = {

			'tags':tag_list

		}

		return render(request, 'tags/lista.html', context)