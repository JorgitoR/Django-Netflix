from django import template
from django.contrib.contenttypes.models import ContentType

from clasificacion.models import Clasificacion
from clasificacion.forms import ClasificacionForm

register = template.Library()

@register.inclusion_tag('clasificacion/rating.html', takes_context=True)
def clasificar(context, *args, **kwargs):


	obj = kwargs.get("object")
	print(obj)

	solo_clasificacion = kwargs.get("solo_clasificacion")
	print('Puntaje', solo_clasificacion)
	request = context['request']
	usuario = None
	if request.user.is_authenticated:
		usuario = request.user
	app_label = obj._meta.app_label #playlist
	model_name = obj._meta.model_name #playlist

	prt = f"app_label: {app_label}, model_name: {model_name}"

	print(prt)

	if app_label == "playlist":
		if model_name =='movieproxy' or 'tvshowproxy':
			model_name = 'playlist'

	c_type = ContentType.objects.get(app_label=app_label, model=model_name)
	avg_clasificacion = Clasificacion.objects.filter(
						content_type=c_type, 
						object_id=obj.id
					).rating()
	# 

	print(args, kwargs)

	context = {
		'value': avg_clasificacion,
		'form':None
	}

	mostrar_form = False
	if usuario is not None:
		mostrar_form = True
	if solo_clasificacion is True:
		mostrar_form = False

	if mostrar_form:
		context['form'] = ClasificacionForm(initial={

			"object_id":obj.id,
			"content_type_id":c_type.id,
			"siguiente":request.path

			})
		
	#if avg_clasificacion is None:
	#	avg_clasificacion = 0

	return context