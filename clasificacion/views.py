from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType 
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ClasificacionForm
from .models import Clasificacion


def clasificar_object_view(request):
	if not request.user.is_authenticated:
		return  HttpResponseRedirect('/')
	if request.method == "POST":
		form = ClasificacionForm(request.POST)
		if form.is_valid():
			object_id = form.cleaned_data.get('object_id')
			clasificar = form.cleaned_data.get('clasificacion')
			content_type_id = form.cleaned_data.get('content_type_id')
			c_type = ContentType.objects.get_for_id(content_type_id)
			obj = Clasificacion.objects.create(
					usuario=request.user,
					valor = clasificar,
					content_type = c_type,
					object_id = object_id
			)

			siguiente_ruta = form.cleaned_data.get('siguiente') #detail View
			print(siguiente_ruta)
			return HttpResponseRedirect(siguiente_ruta)

	return HttpResponseRedirect('/')











