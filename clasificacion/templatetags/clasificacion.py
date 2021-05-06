from django import template
from django.contrib.contenttypes.models import ContentType

from clasificacion.models import Clasificacion

register = template.Library()

@register.inclusion_tag('clasificacion/rating.html')
def clasificar(*args, **kwargs):


	obj = kwargs.get("object")
	print(obj)
	app_label = obj._meta.app_label #playlist
	model_name = obj._meta.model_name #playlist
	c_type = ContentType.objects.get(app_label=app_label, model_name=model_name)
	avg_clasificacion = Clasificacion.objects.filter(content_type=c_type, object_id=obj.id)

	print(args, kwargs)
	return {
		"value": 1
	}