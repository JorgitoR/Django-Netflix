import random
import string
from django.utils.text import slugify


def obtener_string_aleatorios(size=4, letras=string.ascii_lowercase + string.digits):
	return "".join([random.choice(letras) for _ in range(size)])


def obtener_unica_slug(instance, nueva_slug=None, size=10, maximo_size=30):
	titulo = instance.titulo

	if nueva_slug is None:
		"""
		Defecto
		"""
		slug = slugify(titulo)

	else:
		"""
		Recursive
		"""
		slug = nueva_slug

	slug = slug[:maximo_size]
	Klass = instance.__class__ #PlayList, Categoria
	padre = None
	try:
		padre = instance.padre
	except:
		pass

	if padre is not None:
		qs = Klass.objects.filter(padre=padre, slug=slug) #smaller
	else:
		qs = Klass.objects.filter(slug=slug) #large

	if qs.exists():
		nueva_slug = slugify(titulo) + obtener_string_aleatorios(size=size)
		return obtener_unica_slug(instance, nueva_slug=nueva_slug)
	return slug
