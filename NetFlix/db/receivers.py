from .models import PublishStateOptions
from django.utils.text import slugify
from django.utils import timezone


def publicado_stado_pre_save(sender, instance, *args, **kwargs):

	publicado  = instance.stado == PublishStateOptions.PUBLISH
	draft = instance.stado == PublishStateOptions.DRAFT

	if publicado and instance.tiempo_publicado is None:
		print("Guardado el tiempo de publicado")
		instance.tiempo_publicado = timezone.now()

	elif draft:
		instance.tiempo_publicado = None


def slugify_pre_save(sender, instance, *args, **kwargs):
	titulo = instance.titulo
	slug = instance.slug 
	if slug is None:
		instance.slug = slugify(titulo)